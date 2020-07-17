import os
import shutil
import exifread
import datetime



def sort_photos():
    source = r"E:/Nikon/Unsorted/"
    destination = r"E:/Nikon/Sorted"
    entries = os.listdir(source)
    for entry in entries:
        if os.path.isfile(source+entry):
            f = open(source+entry, 'rb')
            tags = exifread.process_file(f, details=False)
            f.close()
            photo_date = tags["Image DateTime"]
            year = str(photo_date)[0:4]
            month_int = int(str(photo_date)[5:7])
            month = datetime.date(1900, month_int, 1).strftime('%B')
            folder = destination+"/"+year+"/"+month+"/"
            if not os.path.exists(folder):
                os.makedirs(folder)
            print(folder+entry)
            shutil.move(source+entry, folder+entry)
sort_photos()
