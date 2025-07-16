import os
import shutil
import datetime
import logging
import exifread

SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.nef', '.cr2', '.raw']

def get_exif_date(file_path):
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, stop_tag="EXIF DateTimeOriginal", details=False)
            date_taken = tags.get("EXIF DateTimeOriginal")
            if date_taken:
                date_str = str(date_taken)
                return datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        logging.warning(f"EXIF read failed for {file_path}: {e}")
    return None

def get_modified_date(file_path):
    timestamp = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(timestamp)

def create_destination_path(base_path, date_obj, structure="YM"):
    if structure == "YM":
        return os.path.join(base_path, str(date_obj.year), f"{date_obj.month:02d}")
    elif structure == "YMD":
        return os.path.join(base_path, str(date_obj.year), f"{date_obj.month:02d}", f"{date_obj.day:02d}")
    else:
        raise ValueError("Invalid folder structure type")

def sort_photos(source_dir, destination_dir, process_type="copy", folder_struct="YM"):
    total = 0
    success = 0
    errors = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            total += 1
            ext = os.path.splitext(file)[1].lower()
            if ext not in SUPPORTED_FORMATS:
                continue

            src_file_path = os.path.join(root, file)

            try:
                date_taken = get_exif_date(src_file_path) or get_modified_date(src_file_path)
                dest_folder = create_destination_path(destination_dir, date_taken, structure=folder_struct)
                os.makedirs(dest_folder, exist_ok=True)
                dest_file_path = os.path.join(dest_folder, file)

                if process_type == "copy":
                    shutil.copy2(src_file_path, dest_file_path)
                elif process_type == "move":
                    shutil.move(src_file_path, dest_file_path)
                else:
                    raise ValueError("Invalid process type")

                success += 1
            except Exception as e:
                logging.error(f"Error processing {src_file_path}: {e}")
                errors += 1

    return total, success, errors
