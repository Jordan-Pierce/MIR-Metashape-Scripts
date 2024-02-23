# Mission: Iconic Reefs Agisoft Metashape API Scripts  (in progress)

<p align="center">
  <img src="./Figures/MIR_Logo.png" alt="MIR_Logo">
</p>
  
This repository contains the code described in the [Mission: Iconic Reef (MIR) Large Area Imaging (LAI) Guide]() and can be used to create large 3D reconstructed underwater scenes. The purpose of these scripts is to streamline and standardize, as much as possible, the processing of hundreds of LAI datasets

For more information, please visit the [NOAA website](https://www.fisheries.noaa.gov/southeast/habitat-conservation/restoring-seven-iconic-reefs-mission-recover-coral-reefs-florida-keys). 

## Workflow 

The workflow consists of `5` parts, and can be run from within Metashape using the `Script` tool. The scripted steps (see below) can be used to reconstuct an individual scene, or multiple scenes in succession; this is done by repeatedly running the respective script in a **loop**, one after the other.  

**The steps include:**  
1. Within Metashape `Scripts`, or via commandline, run script `MIR_Metashape_Processing_I.py`
   - This will run all necessary steps from importing cameras, alignment, detecting markers, to alignment
   - Note that this script can process multiple scenes
2. Within Metashape, manually define ground control points (i.e., markers), if applicable
3. Within Metashape `Scripts`, or via commandline, run script `MIR_Metashape_Processing_II.py`
    - This will run all necessary steps from optimizing camera alignment, filtering points based on uncertainty, to creating a dense point cloud
   - Note that this script can process multiple scenes
5. Within Metashape, manually inspect Dense Cloud and define the scene's bounding polygon to reduce excess space
6. Within Metashape `Scripts`, or via commandline, run script `MIR_Metashape_Processing_III.py`
    - This will run all necessary steps for creating a DEM, mesh, and orthomosaic, and exporting the data products to disk
   - Note that this script can process multiple scenes
  
For more details on each script, please the [instructions](./Scripts/README.md) in the `Scripts` folder.

### Metashape Version

The scripts in this workflow use Metashape 1.8.4; because of updates, using other versions might cause the scripts to fail.
Below are links to the Metashape Desktop, and wheels to the Metashape Python API:
- [Metashape Desktop 1.8.4 (Windows)](https://s3-eu-west-1.amazonaws.com/download.agisoft.com/metashape-pro_1_8_4_x64.msi)
- [Metashape Python API 1.8.4 (Windows)](https://github.com/Jordan-Pierce/MIR-Metashape-Scripts/blob/main/Packages/Metashape-1.8.4-cp35.cp36.cp37.cp38-none-win_amd64.whl)

---

### Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an 'as is' basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.


### License 

Software code created by U.S. Government employees is not subject to copyright in the United States (17 U.S.C. §105). The United States/Department of Commerce reserve all rights to seek and obtain copyright protection in countries other than the United States for Software authored in its entirety by the Department of Commerce. To this end, the Department of Commerce hereby grants to Recipient a royalty-free, nonexclusive license to use, copy, and create derivative works of the Software outside of the United States.