import os
import json

for name in os.listdir(".\BlobFolder"):
    appID = name.split(" ")[0]
    mainFolder =".\BlobFolder\\"+appID+" folder\\"
    workingFolder = mainFolder + appID+" unpacked\\"
    toOpen = "CanvasManifest.json"
    if(len(os.listdir(workingFolder))>0):
        f = open(workingFolder + toOpen,encoding='utf8')
        data = json.load(f)