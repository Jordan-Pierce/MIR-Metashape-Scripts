## This script comes from this forum thread: https://www.agisoft.com/forum/index.php?topic=13046.0
## Adapted for Mission: Iconic Reefs
## Mike Bollinger
## 9/1/2022

import Metashape
import os, sys



def cameraMarkerClear():
    print("Clearing markers from selected cameras...", flush=True)
    #doc = Metashape.app.document
    chunk = Metashape.app.document.chunk
    countCams = 0
    countMarks = 0
    for camera in chunk.cameras:
        if camera.selected:
            countCams = countCams + 1
            for marker in chunk.markers:
                proj = marker.projections[camera]
                if proj is not None:
                    if not proj.pinned: ##"If not" selects BLUE flags, "If" Selects Green Flags
                        countMarks = countMarks + 1
                        marker.projections[camera] = None
                        print("removing " + marker.label + " from " + camera.label, flush=True)

    print("Removed " + str(countMarks) + " markers from " + str(countCams) + " cameras.")


Metashape.app.addMenuItem("Reference Tools/Clear Markers From Selected Cameras", cameraMarkerClear)