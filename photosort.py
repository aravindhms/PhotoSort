import os
import shutil
import datetime
import exifread

# source = r"E:/Nikon/Unsorted/"
# destination = r"E:/Nikon/Sorted"
image_formats = ["JPEG", "JPG", "PNG", "RAW", "NEF","CR2"]
# process_type = 'copy'


def sort_photos(source_folder, destination_folder, process_type,folder_struct):
    process_count = 0
    error_count = 0
    print(folder_struct)
    entries = os.listdir(source_folder)
    for entry in entries:
        if entry.upper().endswith(tuple(image_formats)):
            try:
                f = open(source_folder + entry, 'rb')
                tags = exifread.process_file(f, details=False)
                f.close()
                photo_date = tags["EXIF DateTimeOriginal"]
                year = str(photo_date)[0:4]
                month_int = int(str(photo_date)[5:7])
                month = datetime.date(1900, month_int, 1).strftime('%B')
                day = str(photo_date)[8:10]
                if folder_struct == 'YM':
                    folder = destination_folder + "/" + year + "/" + month + "/"
                if folder_struct == 'YMD':
                    folder = destination_folder + "/" + year + "/" + month + "/"+ day + "/"
                if not os.path.exists(folder):
                    os.makedirs(folder)
                if process_type == 'move':
                    shutil.move(source_folder + entry, folder + entry)
                    process_count = process_count+1
                if process_type == 'copy':
                    shutil.copy(source_folder + entry, folder + entry)
                    process_count = process_count + 1
            except Exception as e:
                print(entry, e)
                error_count = error_count+1
    return process_count, error_count


# sort_photos(source, destination,process_type)


def image_count(source_folder):
    count = 0
    entries = os.listdir(source_folder)
    for entry in entries:
        if entry.upper().endswith(tuple(image_formats)):
            count = count+1
    return count
