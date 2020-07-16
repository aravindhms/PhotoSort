import os
import shutil


source = r"E:/Nikon/Sorted/2020/May/"

entries = os.listdir(source)
for entry in entries:
    if os.path.isfile(source+entry):
        if r' (1)' in entry:
            newname=entry[0:8]+".NEF"
            shutil.move(source + entry, source + newname)
