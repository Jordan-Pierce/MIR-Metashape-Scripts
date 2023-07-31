import Metashape
import math
import os
import json

doc = Metashape.app.document
chunk = Metashape.app.document.chunk # FIXME this is just the active chunk
cams = chunk.cameras

proj_path = doc.path
proj_dir, proj_name = os.path.split(proj_path)
proj_name = proj_name[:-4]

outputs = {}

cams_filename = proj_dir + '/' + proj_name + '.cams.xml'
meta_filename = proj_dir + '/' + proj_name + '.meta.json'

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
    
    outputs[key] = {'path' : path, 'center' : center, 'transform' : trans}
    
	
print(outputs)
meta_file.write(json.dumps({'cameras' : outputs}, indent=4))

meta_file.close()
print("Finished Exporting Cams")
