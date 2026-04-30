# 📸 PhotoSort

**PhotoSort** is a simple Python tool to organize your photos based on their EXIF metadata.  
It can automatically sort images into folders like `Year/Month` or `Year/Month/Day` using a command-line interface (CLI).

---

## ✨ Features

- ✅ Sort by photo capture date (EXIF)  
- ✅ Choose between `copy` or `move`  
- ✅ Organize into `Year/Month` or `Year/Month/Day` folders  
- ✅ Command-line interface (CLI) for automation  
- ✅ Supports JPEG, JPG, PNG, RAW, NEF, CR2 formats

---

## 🚀 Installation

1. Clone or download this repo:

    `git clone https://github.com/aravindhms/PhotoSort.git`  
    `cd PhotoSort`

2. Install dependencies:

    `pip install -r requirements.txt`

---

## 🖥️ Usage

### 📌 Option 1: Windows Executable (EXE)

Download the latest exe from [releases](https://github.com/aravindhms/PhotoSort/releases)

### 📌 Option 2: Command-Line Interface (CLI)

Run with:

    python main.py -s <source_path> -d <destination_path> -t <copy|move> -f <YM|YMD>

**Examples:**

    python main.py -s "E:/Camera/Unsorted" -d "E:/Camera/Sorted" -t copy -f YMD

---

## 📌 Programmatic API

If you prefer to use the core logic directly from Python, call the helper in `photosort.py`:

    from photosort import sort_photos

    total, success, errors = sort_photos(
        source_dir="/path/to/source",
        destination_dir="/path/to/destination",
        process_type="copy",       # or "move"
        folder_struct="YM"         # or "YMD"
    )

This returns a tuple: `(total_files_scanned, successfully_sorted, errors)`.

---

## 📁 Folder Structure

    PhotoSort/
    ├── photosort.py          # Core logic
    ├── main.py               # CLI entry point
    ├── requirements.txt      # Dependencies
    ├── README.md             # This file

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License
