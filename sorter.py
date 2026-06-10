import os
import shutil
import datetime
import exifread
import logging
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

SUPPORTED_FORMATS = {
    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic', '.tiff', '.bmp',
    # RAW Images
    '.nef', '.cr2', '.raw', '.arw', '.dng',
    # Videos
    '.mp4', '.mov', '.avi', '.mkv', '.wmv'
}
HISTORY_FILE = "history.json"

def get_file_hash(file_path):
    """Calculate MD5 hash of a file for duplicate detection."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"Failed to hash {file_path}: {e}")
        return None

def get_exif_date(file_path):
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, stop_tag="EXIF DateTimeOriginal", details=False)
            date_taken = tags.get("EXIF DateTimeOriginal")
            if date_taken:
                date_str = str(date_taken)
                return datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        pass
    return None

def get_modified_date(file_path):
    timestamp = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(timestamp)

def create_destination_path(base_path, date_obj, structure="YM", ext=""):
    if structure == "FLAT":
        return base_path
    
    if not date_obj and structure not in ["EXT", "FLAT"]:
        date_obj = datetime.datetime.now()

    if structure == "YM":
        return os.path.join(base_path, str(date_obj.year), f"{date_obj.month:02d}")
    elif structure == "YMD":
        return os.path.join(base_path, str(date_obj.year), f"{date_obj.month:02d}", f"{date_obj.day:02d}")
    elif structure == "Y":
        return os.path.join(base_path, str(date_obj.year))
    elif structure == "YMN":
        return os.path.join(base_path, str(date_obj.year), date_obj.strftime("%B"))
    elif structure == "EXT":
        return os.path.join(base_path, ext.upper().replace('.', ''))
    elif structure == "YEXT":
        return os.path.join(base_path, str(date_obj.year), ext.upper().replace('.', ''))
    else:
        raise ValueError("Invalid folder structure type")

def get_all_supported_files(source_dir):
    files_to_process = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_FORMATS:
                files_to_process.append(os.path.join(root, file))
    return files_to_process

def process_single_file(src_file_path, destination_dir, process_type, folder_struct, prefix, dry_run):
    file_name = os.path.basename(src_file_path)
    base, ext = os.path.splitext(file_name)
    
    # Custom Naming Convention
    if prefix:
        file_name = f"{prefix}_{file_name}"
        
    date_taken = get_exif_date(src_file_path) or get_modified_date(src_file_path)
    dest_folder = create_destination_path(destination_dir, date_taken, structure=folder_struct, ext=ext)
    
    if not dry_run:
        os.makedirs(dest_folder, exist_ok=True)
        
    dest_file_path = os.path.join(dest_folder, file_name)

    # Duplicate Detection
    if os.path.exists(dest_file_path):
        src_hash = get_file_hash(src_file_path)
        dest_hash = get_file_hash(dest_file_path)
        if src_hash == dest_hash:
            # True duplicate, skip
            return {"file": file_name, "type": "success", "msg": "Skipped true duplicate", "history": None}
        else:
            # Same name, different content. Append counter.
            counter = 1
            while os.path.exists(dest_file_path):
                dest_file_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                counter += 1

    history_record = {
        "original_path": src_file_path,
        "new_path": dest_file_path,
        "process_type": process_type
    }

    if not dry_run:
        # Safe Move / Copy
        if process_type == "copy":
            shutil.copy2(src_file_path, dest_file_path)
        elif process_type == "move":
            # Safe Move logic
            shutil.copy2(src_file_path, dest_file_path)
            if get_file_hash(src_file_path) == get_file_hash(dest_file_path):
                os.remove(src_file_path)
            else:
                raise Exception("Safe move failed: file hashes do not match after copy.")
    else:
        # Dry Run Simulation
        pass

    return {"file": file_name, "type": "success", "history": history_record}

def sort_photos_generator(source_dir, destination_dir, process_type="copy", folder_struct="YM", prefix="", dry_run=False):
    files_to_process = get_all_supported_files(source_dir)
    total = len(files_to_process)
    success = 0
    errors = 0
    job_history = []

    if total == 0:
        yield {"status": "done", "total": 0, "success": 0, "errors": 0}
        return

    yield {"status": "start", "total": total}

    current_idx = 0
    
    # Parallel Processing
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        futures = {
            executor.submit(process_single_file, fp, destination_dir, process_type, folder_struct, prefix, dry_run): fp
            for fp in files_to_process
        }

        for future in as_completed(futures):
            current_idx += 1
            try:
                result = future.result()
                success += 1
                if result.get("history") and not dry_run:
                    job_history.append(result["history"])
                
                yield {
                    "status": "progress",
                    "current": current_idx,
                    "total": total,
                    "file": result["file"],
                    "type": "success"
                }
            except Exception as e:
                errors += 1
                yield {
                    "status": "progress",
                    "current": current_idx,
                    "total": total,
                    "file": os.path.basename(futures[future]),
                    "type": "error",
                    "msg": str(e)
                }

    if not dry_run and job_history:
        with open(HISTORY_FILE, "w") as f:
            json.dump(job_history, f)

    yield {
        "status": "done",
        "total": total,
        "success": success,
        "errors": errors
    }

def undo_last_sort_generator():
    if not os.path.exists(HISTORY_FILE):
        yield {"status": "done", "total": 0, "success": 0, "errors": 0, "msg": "No history found."}
        return

    with open(HISTORY_FILE, "r") as f:
        job_history = json.load(f)

    total = len(job_history)
    success = 0
    errors = 0
    directories_to_check = set()

    if total == 0:
        yield {"status": "done", "total": 0, "success": 0, "errors": 0}
        return

    yield {"status": "start", "total": total}

    for current_idx, record in enumerate(job_history, 1):
        original = record["original_path"]
        new_path = record["new_path"]
        ptype = record["process_type"]
        file_name = os.path.basename(new_path)
        dest_dir = os.path.dirname(new_path)
        
        directories_to_check.add(dest_dir)

        try:
            if not os.path.exists(new_path):
                raise Exception(f"File {new_path} not found.")

            if ptype == "copy":
                os.remove(new_path)
            elif ptype == "move":
                # Ensure directory exists for moving back
                os.makedirs(os.path.dirname(original), exist_ok=True)
                shutil.copy2(new_path, original)
                if get_file_hash(original) == get_file_hash(new_path):
                    os.remove(new_path)
                else:
                    raise Exception("Hash mismatch while undoing move.")

            success += 1
            yield {
                "status": "progress",
                "current": current_idx,
                "total": total,
                "file": file_name,
                "type": "success"
            }
        except Exception as e:
            errors += 1
            yield {
                "status": "progress",
                "current": current_idx,
                "total": total,
                "file": file_name,
                "type": "error",
                "msg": str(e)
            }

    # Clean up empty directories created by the sort
    for d in sorted(list(directories_to_check), key=len, reverse=True):
        try:
            current_d = d
            while current_d and os.path.isdir(current_d):
                if not os.listdir(current_d):
                    os.rmdir(current_d)
                    current_d = os.path.dirname(current_d)
                else:
                    break
        except Exception:
            pass

    # Clear history after successful undo
    if errors == 0:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)

    yield {
        "status": "done",
        "total": total,
        "success": success,
        "errors": errors
    }
