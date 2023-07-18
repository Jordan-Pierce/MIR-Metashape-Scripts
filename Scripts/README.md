# Scripts

Here we describe the MIR Metashape workflow in more detail.

### Expected Folder Structure

Below we explain the expected folder structure. Each script expects each site's images to be in 
its own respective subdirectory; for example, below it can be seen that within the root 
directory, a folder called `Raw_Imagery` contains subdirectories for each site, each of which 
contains the associated images.

After running the script, a separate directory called `Agisoft_Metashape_Data_Exports` within the 
root directory will be created, and will contain the output from Metashape for each site. The 
output includes the project.psx file, associated project metadata, as well as the data products.

```python
./Root_Directory

    /Raw_Imagery
    # Existing directory containing subdirectories of Scene's images
        
        /Site_Plot_YYYMMDD (i.e., EDR_R1-5_20230705)
        # Subdirectory for Scene 1 imagery
            /img_1.jpg
            /img_2.jpg
            ...
        
        /Site_Plot_YYYMMDD (i.e., JPP_P6-7_19930706)
        # Subdirectory for Scene 2 imagery
            /img_1.jpg
            /img_2.jpg
            ...
        ...
        
    /Agisoft_Metashape_Data_Exports 
    # Automatically created with first run of script
        
        /Site_Plot_YYYMMDD (i.e., EDR_R1-5_20230705)
        # Subdirectory for output for Scene 1 
            /project.psx
            /dense_cloud.ply
            /orthomosaic.tif
            ...
        
        /Site_Plot_YYYMMDD (i.e., JPP_P6-7_19930706)
        # Subdirectory for output for Scene 2 
            /project.psx
            /dense_cloud.ply
            /orthomosaic.tif
            ...
        ...
```

## Dependencies 

Some dependencies are required to run these scripts; this includes `dill`, `exif`, `exifread`, `psutil`, and `pandas`.
To install these, you can use package installer for python (`pip`) by doing the following within your python 
environment:
```python
# commandline
pip install dill exif exifread psutils pandas
```

Altneratively, we also include a `requirements.txt` file that can be used to install them for you by doing the following:
```python
# commandline
pip install -r requirements.txt
```

If running entirely from the command line, make sure to also install Metashape, which is located in the `Packages` 
folder in the root of the repository:
```python
# commandline
pip install Packages/Metashape-1.8.4-cp35.cp36.cp37.cp38-none-win_amd64
```
As well as activate the license within your python environment:
```python
# python terminal
import Metashape
Metashape.License().activate("####-####-####")
```

## Script Explanation 

### Metashape Processing Scripts

[`MIR_Metashape_Processing_Part_I.py`](scripts/MIR_Metashape_Processing_Part_I.py)  
This script is used to start the Agisoft Metashape workflow (NCCOS SOP for Agisoft Metashape, 
  Part I: SPC Generation) in Agisoft Metashape Professional Version 1.8.4 . This script brings 
  in the images, imports them into a chunk, and Photo alignment matches detected features 
  across a collection of photos to estimate the position and orientation of each image. This 
process results in the creation of a sparse point cloud (SPC).

[`MIR_Metashape_Processing_Part_II.py`](scripts/MIR_Metashape_Processing_Part_II.py)  
This script is used to run through an error reduction routine, optimize camera alignment, 
  remove erroneous points from the SPC and resize the region before building a dense point 
  cloud (DPC; see NCCOS SOP for Agisoft Metashape, `Part III: Optimization and Error Reduction and 
  Part IV: Building the DPC`). Thresholds for Reconstruction Uncertainty, Projection Accuracy, 
Reprojection Error are defined at the beginning of the script as percentages and target  
  thresholds to not cross.   

After creating the DPC, the script exports the camera locations in 
  the local coordinate system (for Viscore), duplicates the chunk and generates a report. 
  Error reduction ensures that SPC geometry is as accurate as possible by optimizing the 
  camera calibration through an error reduction procedure. Points with reconstruction 
  uncertainty, projection accuracy, and reprojection error are iteratively removed and the SPC 
  geometry is optimized at each iteration. This may be accomplished manually or via scripts. A 
  3D DPC is created by calculating the depth information for each camera based on estimated 
  camera positions. The DPC can then be used for additional steps in the Metashape workflow 
  such as building a DEM (`Part V: Building the DEM and Orthomosaic`). Note that building the 
  DPC is a computationally intensive process that requires computational resources and time to 
  complete.

[`scripts/MIR_Metashape_Processing_Part_III.py`](MIR_Metashape_Processing_Part_III.py)  
This script is used to build a Digital Elevation Model (DEM) and an Orthomosic from a 
georeferenced dense point cloud (DPC, see NCCOS SOP for Agisoft Metashape, Part V: Building the 
DEM and Orthomosaic). There is an option to also build a tiled model. Another Report is 
generated, but adding metadata on the orthomosaic and DEM. A DEM represents a surface model as 
a grid of height values. DPCs built in `Part IV: Building the DPC` are georeferenced with 
geographic coordinates from the field before a DEM is processed. High resolution top-down 2D 
map views, known as Orthomosiacs (or orthophotomosaics), are created based on the source photos 
and the reconstructed model. 

### Running Metashape Scripts

All Metashape scripts require a single `--input` argument, representing the path(s) to the one or more folders of images you 
want to process. The `--input` argument expects one of the following:
```python
# commandline

# Example 1 - single site
python MIR_Metashape_Processing_1.py  --input "C:\\Users\\UserData\\MIR\\Raw_Imagery\\EDR_R1-5_20230705\\"

# Example 2 - multiple sites 
python MIR_Metashape_Processing_1.py  --input "C:\\Users\\UserData\\MIR\\Raw_Imagery\\EDR_R1-1_20230705\\" \
                                              "C:\\Users\\UserData\\MIR\\Raw_Imagery\\EDR_R1-2_20230705\\" \
                                              "C:\\Users\\UserData\\MIR\\Raw_Imagery\\EDR_R1-3_20230705\\"

# Example 3 - one or more sites whose paths are in a text file
python MIR_Metashape_Processing_1.py --input site_list.txt

```

Where the site list should be formatted as below:
```
# site_list.txt
C:\UserData\MissionIconicReefs\Raw_Imagery\EDR_R1-5_20230705
C:\UserData\MissionIconicReefs\Raw_Imagery\EDR_R1-3_20230705
C:\UserData\MissionIconicReefs\Raw_Imagery\EDR_R4-5_20230706
C:\UserData\MissionIconicReefs\Raw_Imagery\EDR_R4-3_20230706
```


### Miscellaneous Scripts

[`remove_blue_flags.py`](scripts/remove_blue_flags.py)  
This script, adapted from an Agisoft forum post, is meant to remove blue flag markers. In the 
  camera optimization step, Agisoft takes into account the location of both the green and blue 
  flag markers to determine the correct location. This script is meant to eliminate the blue 
  flags and let Agisoft use only the user defined green flags in the coordinate solution. 

[`image_rotator.py`](scripts/image_rotator.py)  
This script is used to rotate images to the orientation in which they were captured. Depending 
  on the camera model used, images will be displayed in either landscape or portrait mode with 
  varying degrees of rotation from the orientation in which they were collected (i.e., 90 
  degrees, 180 degrees, 270 degrees). If Viscore is used for later analysis, it is preferable 
  for the images to be in the orientation they were captured in (i.e., landscape with no 
  rotation) before conducting the steps described in `Part I: SPC Generation in Metashape`.

```python 
# commandline
B:\MIR-Metashape-Scripts\Scripts\scripts>python image_rotator.py --input "E:\Raw_Imagery\Site_Images"
```
```python
# Expected output:
* Parallel processing
* Running on 8 cores
* Number of tasks: 77
File Name: E:\Raw_Imagery\Test_Images\DSC_7150.JPG
File Name: E:\Raw_Imagery\Test_Images\DSC_7167.JPG
File Name: E:\Raw_Imagery\Test_Images\DSC_7184.JPG
...
File Name: E:\Raw_Imagery\Test_Images\DSC_8408.JPG
File Name: E:\Raw_Imagery\Test_Images\DSC_8425.JPG
File Name: E:\Raw_Imagery\Test_Images\DSC_8442.JPG
done
```

[`extract_meta.py`](scripts/extract_meta.py)  
This script is used to export specific 3D model data that will be used in the Viscore workflow 
  (NCCOS 2023). The data are exported as three files: .ply, .meta.json, and .cams.xml. A .ply 
  file is converted to a Viscore-compatible format (.vml) so that point data may be visualized 
  in Viscore, and .meta.json and .cams.xml files are used to link raw images to the model. 