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

## Running Scripts

All single-site scripts receive a single input, which the path to the folder containing the images 
to be processed by Metashape:
```python
# commandline
python script_name.py C:\Users\UserData\MIR\Raw_Imagery\EDR_R1-5_20230705\
```

If processing multiple sites in a loop, the expected input is a .txt file containing each folder
containing site's images, seperated by a new-line:
```
# site_list.txt
C:\UserData\MissionIconicReefs\Raw_Imagery\EDR_R1-5_20230705
C:\UserData\MissionIconicReefs\Raw_Imagery\EDR_R1-3_20230705
C:\UserData\MissionIconicReefs\Raw_Imagery\EDR_R4-5_20230706
C:\UserData\MissionIconicReefs\Raw_Imagery\EDR_R4-3_20230706
```

The commandline command then changes to:
```python
# commandline
python script_name.py C:\Users\UserData\MIR\site_list.txt
```

## Script Explanation  

[`MIRmetashapeprocessing_PartI_PhotosToAlignment_v4.py`](MIRmetashapeprocessing_PartI_PhotosToAlignment_v4.py)  
This script is used to start the Agisoft Metashape workflow (NCCOS SOP for Agisoft Metashape, 
  Part I: SPC Generation) in Agisoft Metashape Professional Version 1.8.4 . This script brings 
  in the images, imports them into a chunk, and Photo alignment matches detected features 
  across a collection of photos to estimate the position and orientation of each image. This 
process results in the creation of a sparse point cloud (SPC).

[`MIRmetashapeprocessing_PartI-LOOP_v4.py`](MIRmetashapeprocessing_PartI-LOOP_v4.py)    
This script is used to process SPC Generation for two or more plots sequentially. A text file 
  containing the file paths for the image folders is created and the path for the .txt file is 
  used as the arguments. 

[`MIRmetashapeprocessing_PartII_MarkersToDense_v7.py`](MIRmetashapeprocessing_PartII_MarkersToDense_v7.py)  
This script is used to run through an error reduction routine, optimize camera alignment, 
  remove erroneous points from the SPC and resize the region before building a dense point 
  cloud (DPC; see NCCOS SOP for Agisoft Metashape, Part III: Optimization and Error Reduction and 
  Part IV: Building the DPC). Thresholds for Reconstruction Uncertainty, Projection Accuracy, 
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
  such as building a DEM (Part V: Building the DEM and Orthomosaic). Note that building the 
  DPC is a computationally intensive process that requires computational resources and time to 
  complete.

[`MIRmetashapeprocessing_PartII_LOOP_v6.py`](MIRmetashapeprocessing_PartII_LOOP_v6.py)  
This script is used to process optimization, error reduction and build a DPC for two or more 
  plots sequentially. A text file containing the file paths for the image folders is created and 
  the path for the .txt file is used in the arguments. 

[`MIRmetashapeprocessing_PartIII_ExportAgisoftProducts_v2.py`](MIRmetashapeprocessing_PartIII_ExportAgisoftProducts_v2.py)  
This script is used to build a Digital Elevation Model (DEM) and an Orthomosic from a 
georeferenced dense point cloud (DPC, see NCCOS SOP for Agisoft Metashape, Part V: Building the 
DEM and Orthomosaic). There is an option to also build a tiled model. Another Report is 
generated, but adding metadata on the orthomosaic and DEM. A DEM represents a surface model as 
a grid of height values. DPCs built in Part IV: Building the DPC are georeferenced with 
geographic coordinates from the field before a DEM is processed. High resolution top-down 2D 
map views, known as Orthomosiacs (or orthophotomosaics), are created based on the source photos 
and the reconstructed model. 

[`MIRmetashapeprocessing_PartIII_LOOP.py`](MIRmetashapeprocessing_PartIII_LOOP.py)  
This script is used to build a DEM and an Orthomosaic for two or more plots sequentially. A 
  text file containing the file paths for the image folders is created and the path for the .
  txt file is used in the arguments. 

[`RemoveBlueFlags.py`](RemoveBlueFlags.py)  
This script, adapted from an Agisoft forum post, is meant to remove blue flag markers. In the 
  camera optimization step, Agisoft takes into account the location of both the green and blue 
  flag markers to determine the correct location. This script is meant to eliminate the blue 
  flags and let Agisoft use only the user defined green flags in the coordinate solution. 

[`rotaterV4.py`](rotaterV4.py)  
This script is used to rotate images to the orientation in which they were captured.Depending 
  on the camera model used, images will be displayed in either landscape or portrait mode with 
  varying degrees of rotation from the orientation in which they were collected (i.e., 90 
  degrees, 180 degrees, 270 degrees). If Viscore is used for later analysis, it is preferable 
  for the images to be in the orientation they were captured in (i.e., landscape with no 
  rotation) before conducting the steps described in Part I: SPC Generation in Metashape.

[`extract_meta_MB.py`](extract_meta_MB.py)  
This script is used to export specific 3D model data that will be used in the Viscore workflow 
  (NCCOS 2023). The data are exported as three files: .ply, .meta.json, and .cams.xml. A .ply 
  file is converted to a Viscore-compatible format (.vml) so that point data may be visualized 
  in Viscore, and .meta.json and .cams.xml files are used to link raw images to the model. 