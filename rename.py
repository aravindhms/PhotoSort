import os
import shutil
import exifread


source = r"D:/Anu Aravindh/1.7.2018/"

entries = os.listdir(source)
for entry in entries:
    if os.path.isfile(source+entry):
        f = open(source + entry, 'rb')
        print(entry)
        tags = exifread.process_file(f, details=False)
        f.close()
        photo_time = str(tags["EXIF DateTimeDigitized"])[11:20]
        photo_date_orig = tags["EXIF DateTimeDigitized"]
        print("2018:07:01 "+photo_time)
