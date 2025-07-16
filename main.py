import argparse
from photosort import sort_photos


def main():
    parser = argparse.ArgumentParser(description="Sort photos by EXIF date into folders.")

    parser.add_argument(
        "-s", "--source", required=True,
        help="Path to the source folder containing photos"
    )
    parser.add_argument(
        "-d", "--destination", required=True,
        help="Path to the destination folder where sorted photos will be stored"
    )
    parser.add_argument(
        "-t", "--type", choices=["copy", "move"], default="copy",
        help="Whether to copy or move files (default: copy)"
    )
    parser.add_argument(
        "-f", "--folder", choices=["YM", "YMD"], default="YM",
        help="Folder structure: YM = Year/Month, YMD = Year/Month/Day"
    )

    args = parser.parse_args()

    print(f"Sorting photos from '{args.source}' to '{args.destination}' using {args.folder} structure...")

    try:
        sort_photos(
            source_folder=args.source,
            destination_folder=args.destination,
            process_type=args.type,
            folder_struct=args.folder
        )
        print("✅ Sorting completed successfully.")
    except Exception as e:
        print(f"❌ Error occurred: {e}")


if __name__ == "__main__":
    main()
