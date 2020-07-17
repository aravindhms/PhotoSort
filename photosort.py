import os
import shutil
import datetime
import exifread

source = r"E:/Nikon/Unsorted/"
destination = r"E:/Nikon/Sorted"
image_formats = ["JPEG", "JPG", "PNG", "RAW", "NEF"]


def sort_photos(source_folder, destination_folder):
    entries = os.listdir(source_folder)
    for entry in entries:
        if os.path.isfile(source_folder + entry):
            f = open(source_folder + entry, 'rb')
            tags = exifread.process_file(f, details=False)
            f.close()
            photo_date = tags["Image DateTime"]
            year = str(photo_date)[0:4]
            month_int = int(str(photo_date)[5:7])
            month = datetime.date(1900, month_int, 1).strftime('%B')
            folder = destination_folder + "/" + year + "/" + month + "/"
            if not os.path.exists(folder):
                os.makedirs(folder)
            print(folder+entry)
            shutil.move(source_folder + entry, folder + entry)


sort_photos(source, destination)


def image_count(source_folder):
    count = 0
    entries = os.listdir(source_folder)
    for entry in entries:
        if entry.endswith(tuple(image_formats)):
            count = count+1
    return count


def check_exif(source_folder):
    entries = os.listdir(source_folder)
    for entry in entries:
        if entry.endswith(tuple(image_formats)):
            count = count+1
    return count
