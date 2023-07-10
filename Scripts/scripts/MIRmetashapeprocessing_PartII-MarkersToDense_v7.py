import Metashape
import os, sys
import time, datetime
import math
import json

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
doc = Metashape.app.document
doc.open(export_path + '/' + proj_name + '.psx')
#doc.save(export_path + '/' + proj_name + '.psx')

#doc.save()
#Define which chunk
#chunk = Metashape.app.document.chunk # Active Chunk in GUI

#doc.save(export_path + '/' + proj_name + '.psx')

#chunk = doc.addChunk()
chunk = Metashape.app.document.chunk

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


# Error Reduction
# https://agisoft.freshdesk.com/support/solutions/articles/31000154629-how-to-select-fixed-percent-of-the-points-gradual-selection-using-python

## Reconstruction Uncertainty
chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True,  fit_k1=True, fit_k2=True, fit_k3=True,
                      fit_k4=False, fit_p1=True, fit_p2=True, fit_b1=False, fit_b2=False,
                      fit_corrections=False, adaptive_fitting=False, tiepoint_covariance=False)
print(proj_name + " optimization 1/5 completed")
doc.save()

points = chunk.point_cloud.points
f = Metashape.PointCloud.Filter()
f.init(chunk, criterion = Metashape.PointCloud.Filter.ReconstructionUncertainty) #Reconstruction Uncertainty
list_values = f.values
list_values_valid = list()
StartPoints = len(list_values_valid)

for i in range(len(list_values)):
    if points[i].valid:
        list_values_valid.append(list_values[i])
list_values_valid.sort()
target = int(len(list_values_valid) * RU_Percent / 100)
StartPoints = int(len(list_values_valid))
AlignmentPoints = StartPoints
threshold = list_values_valid[target]
if (threshold < RU_Threshold):
    threshold = RU_Threshold
f.selectPoints(threshold)
f.removePoints(threshold)

print("")
print("Error Reduction Report:")
RU_actual_threshold = threshold
print(str(threshold) + " threshold reached")
print(str(StartPoints) + " points at start")
print(str(target) + " points removed")
print(proj_name + " Reconstruction Uncertainty filter completed")
print("")

## Projection Accuracy
chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True,  fit_k1=True, fit_k2=True, fit_k3=True,
                      fit_k4=False, fit_p1=True, fit_p2=True, fit_b1=False, fit_b2=False,
                      fit_corrections=False, adaptive_fitting=False, tiepoint_covariance=False)
print(proj_name + " optimization 2/5 completed")
doc.save()

points = chunk.point_cloud.points
f = Metashape.PointCloud.Filter()
f.init(chunk, criterion = Metashape.PointCloud.Filter.ProjectionAccuracy) #Projection Accuracy
list_values = f.values
list_values_valid = list()

for i in range(len(list_values)):
    if points[i].valid:
        list_values_valid.append(list_values[i])
list_values_valid.sort()
target = int(len(list_values_valid) * PA_Percent / 100)
StartPoints = int(len(list_values_valid))
threshold = list_values_valid[target]
if (threshold < PA_Threshold):
    threshold = PA_Threshold
f.selectPoints(threshold)
f.removePoints(threshold)

print("")
print("Error Reduction Report:")
PA_actual_threshold = threshold
print(str(threshold) + " threshold reached")
print(str(StartPoints) + " points at start")
print(str(target) + " points removed")
print(proj_name + " Projection Accuracy filter completed")
print("")

## Reprojection Error
chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True,  fit_k1=True, fit_k2=True, fit_k3=True,
                      fit_k4=False, fit_p1=True, fit_p2=True, fit_b1=False, fit_b2=False,
                      fit_corrections=False, adaptive_fitting=False, tiepoint_covariance=False)
print(proj_name + " optimization 3/5 completed")
doc.save()

points = chunk.point_cloud.points
f = Metashape.PointCloud.Filter()
f.init(chunk, criterion = Metashape.PointCloud.Filter.ReprojectionError) #Reprojection Error
list_values = f.values
list_values_valid = list()

for i in range(len(list_values)):
    if points[i].valid:
        list_values_valid.append(list_values[i])
list_values_valid.sort()
target = int(len(list_values_valid) * RE_Percent / 100)
StartPoints = int(len(list_values_valid))
#set threshold
threshold = list_values_valid[target]
if (threshold < RE_Threshold):
    threshold = RE_Threshold
#remove points
f.selectPoints(threshold)
f.removePoints(threshold)

print("")
print("Error Reduction Report:")
RE_actual_threshold = threshold
print(str(threshold) + " threshold reached")
print(str(StartPoints) + " points at start")
print(str(target) + " points removed")
print(proj_name + " Reprojection Error filter 1 completed")
print("")

## Reprojection Error 2
chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True,  fit_k1=True, fit_k2=True, fit_k3=True,
                      fit_k4=True, fit_p1=True, fit_p2=True, fit_b1=True, fit_b2=True,
                      fit_corrections=False, adaptive_fitting=False, tiepoint_covariance=False)
print(proj_name + " optimization 4/5 completed")
doc.save()

points = chunk.point_cloud.points
f = Metashape.PointCloud.Filter()
f.init(chunk, criterion = Metashape.PointCloud.Filter.ReprojectionError) #Reprojection Error
list_values = f.values
list_values_valid = list()

for i in range(len(list_values)):
    if points[i].valid:
        list_values_valid.append(list_values[i])
list_values_valid.sort()
target = int(len(list_values_valid) * RE_Percent / 100)
StartPoints = int(len(list_values_valid))
threshold = list_values_valid[target]
if (threshold < RE_Threshold):
    threshold = RE_Threshold
f.selectPoints(threshold)
f.removePoints(threshold)
EndPoints = int(len(list_values_valid))

print("")
print("Error Reduction Report:")
RE_actual_threshold = threshold
print(str(threshold) + " threshold reached")
print(str(StartPoints) + " points at start")
print(str(target) + " points removed")
print(proj_name + " Reprojection Error filter 2 completed")
print("")

chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True,  fit_k1=True, fit_k2=True, fit_k3=True,
                      fit_k4=True, fit_p1=True, fit_p2=True, fit_b1=True, fit_b2=True,
                      fit_corrections=False, adaptive_fitting=False, tiepoint_covariance=False)
print(proj_name + " optimization 5/5 completed")
doc.save()

# Resize Region
#region = chunk.region
#T = chunk.transform.matrix

#m = Metashape.Vector([10E+10, 10E+10, 10E+10])
#M = -m

#for point in chunk.point_cloud.points:
#    if not point.valid:
#        continue
#    coord = T * point.coord
#    for i in range(3):
#        m[i] = min(m[i], coord[i]) - 0.000015
#        M[i] = max(M[i], coord[i]) + 0.000015

#center = (M + m) / 2
#size = M - m
#region.center = T.inv().mulp(center)
#region.size = size * (1 / T.scale())

#region.rot = T.rotation().t()

#chunk.region = region

# Build Depth Maps
print(proj_name + " Building Depth Maps")
#Note
#For depth maps quality the downscale correspondence should be the following:
#Ultra = 1
#High = 2
#Medium = 4
#Low = 8
#Lowest = 16
chunk.buildDepthMaps(downscale = 2, filter_mode = Metashape.ModerateFiltering)
doc.save()

# Build Dense Cloud
print(proj_name + " Building Dense Cloud")
chunk.buildDenseCloud(point_colors=True, point_confidence=True, keep_depth=True,
                #max_neighbors=100,
                #subdivide_task=True,
                #workitem_size_cameras=20,
                #max_workgroup_size=100
                )
doc.save()
print(proj_name + " Dense Cloud built")

#Export Local points to Viscore
if chunk.dense_cloud:
    chunk.exportPoints(export_path + '/' + proj_name + '.ply',
                       source_data = Metashape.DenseCloudData,
                       save_normals = True,
                       save_colors = True,
                       save_classes = False, #Classes have to be False to see Pt Conf in Viscore
                       save_confidence = True)

#Export Cams to Viscore
cams = chunk.cameras

outputs = {}

cams_filename = export_path + '/' + proj_name + '.cams.xml'
meta_filename = export_path + '/' + proj_name + '.meta.json'

meta_file = open(meta_filename, 'w')

chunk.exportCameras(cams_filename)

for cam in cams:
    key = cam.key
    path = cam.photo.path
    center = cam.center
    if center is not None:
        geo = chunk.transform.matrix.mulp(center)
        if chunk.crs is not None:
            lla = list(chunk.crs.project(geo))
        center = list(center)

    agi_trans = cam.transform
    trans = None
    if agi_trans is not None:
        trans = [list(agi_trans.row(n)) for n in range(agi_trans.size[1])]

    outputs[key] = {'path': path, 'center': center, 'transform': trans}

print(outputs)
meta_file.write(json.dumps({'cameras': outputs}, indent=4))
meta_file.close()
doc.save()


#Duplicate Chunk for Markers and Georeferencing
chunk.copy()
doc.save()


# Export Report
print("Exporting Report")
today = datetime.datetime.now()
# Textual month, day and year
d3 = today.strftime("%B %d, %Y")

chunk.exportReport(path = export_path + '/' + proj_name + '_Report.pdf',
                   title = proj_name,
                   description = "Processing Report: " + d3)


#Define End Time
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
print("Reconstruction Uncertainty Threshold: " + str(RU_Threshold))
print("Projection Accuracy Threshold: " + str(PA_Threshold))
print("Reprojection Error Threshold: " + str(RE_Threshold))
print("Started with " + str(AlignmentPoints) + " points")
print("Ended with " + str(EndPoints) + " points")
print("Break to pick Georeference")
