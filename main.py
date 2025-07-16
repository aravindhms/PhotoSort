# main.py

import argparse
from photosort import sort_photos

def main():
    parser = argparse.ArgumentParser(description="PhotoSort - Organize photos by date taken.")

    parser.add_argument('-s', '--source', required=True, help="Source folder path")
    parser.add_argument('-d', '--destination', required=True, help="Destination folder path")
    parser.add_argument('-t', '--type', choices=['copy', 'move'], default='copy', help="Operation type: copy or move")
    parser.add_argument('-f', '--folder', choices=['YM', 'YMD'], default='YM', help="Folder structure: YM or YMD")

    args = parser.parse_args()

    print(f"\n📁 Source:      {args.source}")
    print(f"📂 Destination: {args.destination}")
    print(f"🔄 Operation:   {args.type}")
    print(f"🗂️ Structure:   {args.folder}")
    print("-" * 40)

    total, success, errors = sort_photos(
        source_dir=args.source,
        dest_dir=args.destination,
        process_type=args.type,
        folder_struct=args.folder
    )

    print(f"\n✅ Total files scanned: {total}")
    print(f"📦 Successfully sorted: {success}")
    print(f"❌ Errors:               {errors}\n")

if __name__ == "__main__":
    main()
