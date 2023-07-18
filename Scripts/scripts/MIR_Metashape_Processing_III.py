import os
import sys
import time
import datetime
import argparse

import Metashape


parser = argparse.ArgumentParser(description='MIR Metashape Processing III')

parser.add_argument('--input', type=str, nargs="+", default=[], required=True,
                    help='Input is one or more paths to input folder(s), '
                         'or a text file containing the paths to one or more input folder(s).')

args = parser.parse_args()

# A list to hold all the paths to sites to loop through
ProcessingQueue = []

# Get the input argument(s)
inputs = args.input

# Make sure user added input, check against default
if not inputs:
    raise Exception("ERROR: No input was provided; ' \
                    please see the help for input instructions")

# Check to see if it's a text file
elif len(inputs) == 1 and ".txt" in inputs[0].lower():
    # Get the text file
    text_file = inputs[0]
    # Make sure it exists
    if not os.path.exists(text_file):
        raise Exception(f"ERROR: The text file provided does not exists {text_file}")

    try:
        # Try opening it and getting each line (folder path), read into list
        with open(text_file, 'r') as file:
            ProcessingQueue = [l.strip().replace("'", "").replace('"', '').replace(" ", "").rstrip('\\/"') for l in
                               file]

        for folder_path in ProcessingQueue:
            if not os.path.exists(folder_path):
                ProcessingQueue.remove(folder_path)
                raise Exception(f"ERROR: The folder path provided does not exists {folder_path}; removing")

    except Exception as e:
        print(f"ERROR: Issue with parsing provided file, please check format of {text_file}\n{e}\n")

# If it's one or more objects, and not a text file, assume it's a or multiple directories
elif len(inputs) >= 1 and ".txt" not in inputs[0].lower():

    for folder_path in inputs:
        # Get the folder path, strip of extra characters just in case
        folder_path = folder_path.rstrip('\\/"')
        # Check that it's a directory and exists
        if not os.path.isdir(folder_path) and not os.path.exists(folder_path):
            raise Exception(f"ERROR: The folder path provided does not exist {folder_path}")
        # Add to processing queue
        ProcessingQueue.append(folder_path)
else:
    raise Exception(f"ERROR: There is something incorrect about your input; please see instructions.")

print("Number of sites to be processed: " + str(len(ProcessingQueue)))

for pq in ProcessingQueue:
    # Define Image Path from user input
    img_path = pq
    proj_dir, jpeg_name = os.path.split(img_path)
    base_dir, img_folder = os.path.split(proj_dir)
    print("proj_dir: " + str(proj_dir))
    print("base_dir: " + str(base_dir))
    print("jpeg_name: " + str(jpeg_name))

    proj_name = str(jpeg_name.rsplit('_', 1)[0])
    print("proj_name: " + str(proj_name))

    export_folder = proj_name
    agisoft_files = "Agisoft_Project_Data_Exports"
    export_path = os.path.join(base_dir, agisoft_files, export_folder)
    print("export_path: " + str(export_path))

    # Define Start Time
    start_time = time.time()
    print_time = time.ctime(start_time)
    print("Start Time: ", print_time)

    # Define which document
    doc = Metashape.app.document
    doc.open(export_path + '/' + proj_name + '.psx')
    # doc.save(export_path + '/' + proj_name + '.psx')
    # doc.save()

    # Define which Chunk
    # chunk = add.Chunk()
    chunk = Metashape.app.document.chunk

    has_transform = chunk.transform.scale and chunk.transform.rotation and chunk.transform.translation

    if has_transform:
        if not chunk.elevation:
            print("Building DEM")
            chunk.buildDem(source_data=Metashape.DenseCloudData)
            doc.save()
            print("Finished DEM")

        if not chunk.orthomosaic:
            print("Building Orthophotomosaic")
            chunk.buildOrthomosaic(surface_data=Metashape.ElevationData)
            doc.save()
            print("Finished building orthophotomosaic")

        # if not chunk.tiled_model:
        #    chunk.buildTiledModel(source_data=Metashape.DenseCloudData)
        #    doc.save()

    ## Export Results
    print("Exporting Products")

    # Export Report
    print("Exporting Report")
    today = datetime.datetime.now()
    # Textual month, day and year
    d3 = today.strftime("%B %d, %Y")

    chunk.exportReport(path=export_path + '/' + proj_name + '_Report.pdf',
                       title=proj_name,
                       description="Processing Report: " + d3)

    # Export DEM
    if chunk.elevation:
        print("Exporting DEM")
        compression = Metashape.ImageCompression()
        compression.tiff_big = True
        chunk.exportRaster(path=export_path + '/' + proj_name + '_DEM.tif',
                           source_data=Metashape.ElevationData,
                           image_compression=compression,
                           north_up=True)
    else:
        print("No DEM Created, none exported")

    # Export Orthophotomosaic
    if chunk.orthomosaic:
        print("Exporting Orthophotomosaic")
        compression = Metashape.ImageCompression()
        compression.tiff_big = True
        chunk.exportRaster(path=export_path + '/' + proj_name + '_Ortho.tif',
                           source_data=Metashape.OrthomosaicData,
                           image_compression=compression,
                           save_kml=False,
                           save_world=False)
    else:
        print("No Orthophotomosaic Created, none exported")

    # Export Tiled Model
    # if chunk.tiled_model:
    #    chunk.exportTiledModel(export_path + '/' + proj_name + '_TiledModel.slpk',
    #                           source_data = Metashape.TiledModel)
    # else:
    #    print("No Tiled Model Created, none exported")

    # Close document to prevent error on next run
    Metashape.Document()

    # Define End Time
    end_time = time.time()
    print_time = time.ctime(end_time)
    print("End Time: ", print_time)
    delta_time = end_time - start_time
    delta_time_hours = datetime.timedelta(seconds=delta_time)
    converted_time = str(delta_time_hours)

    print("")
    print("Processing Report:")
    print("")
    print("Processing Competed In: ", converted_time)

    print('Processing finished, results saved to ' + export_path + '.')

print('Completed all sites in queue')
