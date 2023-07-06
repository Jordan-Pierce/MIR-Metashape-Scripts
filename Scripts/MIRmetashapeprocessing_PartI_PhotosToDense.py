import Metashape
import os, sys
import time, datetime
import math
import json
from csv import writer, DictWriter


if len(sys.argv) > 1:
    # Define Image Path from user input
    img_path = sys.argv[1]
else:
    # Quit if no path given
    print("Please put the path to your image folder in as an argument")
    sys.exit(1)




#Define Image Path from user input
img_path = sys.argv[1]


proj_dir, jpeg_name = os.path.split(img_path)
base_dir, img_folder = os.path.split(proj_dir)
print("proj_dir: " + str(proj_dir))
print("base_dir: " + str(base_dir))
print("jpeg_name: " + str(jpeg_name))

proj_name = str(jpeg_name.rsplit('_',1)[0])
print("proj_name: " + str(proj_name))

export_folder = proj_name
agisoft_files = "Agisoft_Project_Data_Exports"
export_path = os.path.join(base_dir, agisoft_files, export_folder)
print("export_path: " + str(export_path))
#Make sure the export workspace exists.  if not - make them.
if not os.path.exists(export_path):
    os.makedirs(export_path)

##Selection Percentages
RU_Percent = 50
PA_Percent = 50
RE_Percent = 10

## Selection Thresholds
RU_Threshold = 12
PA_Threshold = 3.5
RE_Threshold = 0.9

##Define photos list
photos = [os.path.join(img_path, photo)
        for photo in os.listdir(img_path)
        if photo.endswith('.JPG')]

#Define Start Time
start_time = time.time()
print_time = time.ctime(start_time)
print("Start Time: ", print_time)

#Define which document
doc = Metashape.Document()
#Define which chunk
#chunk = Metashape.app.document.chunk # Active Chunk in GUI

doc.save(export_path + '/' + proj_name + '.psx')

chunk = doc.addChunk()
#Note:
#For matching accuracy the downscale correspondence should be the following:
#Highest = 0
#High = 1
#Medium = 2
#Low = 4
#Lowest = 8
#
#For depth maps quality the downscale correspondence should be the following:
#Ultra = 1
#High = 2
#Medium = 4
#Low = 8
#Lowest = 16

# Add Photos
chunk.addPhotos(photos)
doc.save()

print(str(len(chunk.cameras)) + " images loaded")

# Align Photos
#Note:
#For matching accuracy the downscale correspondence should be the following:
#Highest = 0
#High = 1
#Medium = 2
#Low = 4
#Lowest = 8
chunk.matchPhotos(downscale = 1, #
                  keypoint_limit = 60000,
                  tiepoint_limit = 0,
                  generic_preselection = True,
                  reference_preselection = True)
doc.save()

chunk.alignCameras()
doc.save()


#Detect markers
chunk.detectMarkers(target_type = Metashape.CircularTarget12bit,
              tolerance = 50,
              filter_mask = False,
              inverted = False,
              noparity=False)
doc.save()

#Duplicate Chunk for Markers and Georeferencing
chunk.copy()
doc.save()

#Define End Time
end_time = time.time()
print_time = time.ctime(end_time)
print("End Time: ", print_time)
delta_time = end_time - start_time
delta_time_hours = datetime.timedelta(seconds=delta_time)
converted_time = str(delta_time_hours)

#Write metadata to CSV
#headersCSV = ['Site', 'AlignmentTimer',"RU_Threshold", "PA_Threshold", "RE_Threshold", "AlignmentPoints", "CleanPoints", "DenseTimer"]
#dict = {'Site':proj_name, 'AlignmentTimer':converted_time}

#Make sure the export csv exists. if not - make it
#if not os.path.exists(base_dir + agisoft_files + "/MIRProcessingMetadata.csv"):
#    with open(base_dir + agisoft_files + "/MIRProcessingMetadata.csv", 'a', newline='') as f_object:
#        writer_object = writer(f_object)
#        writer_object.writerow(headersCSV)
#        f_object.close()

#with open(base_dir + agisoft_files + "/MIRProcessingMetadata.csv", 'a', newline='') as f_object:
#    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
#    dictwriter_object.writerow(dict)
#    f_object.close()



print("")
print("Processing Competed In: ", converted_time)
print("")
print("")
print("Break to pick Markers and add Depths")
print("")
print("")


