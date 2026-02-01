# 📸 PhotoSort

**PhotoSort** is a simple Python tool to organize your photos based on their EXIF metadata.  
It can automatically sort images into folders like `Year/Month` or `Year/Month/Day` using a command-line interface (CLI).

---

## ✨ Features

- ✅ Sort by photo capture date (EXIF)  
- ✅ Choose between `copy` or `move`  
- ✅ Organize into `Year/Month` or `Year/Month/Day` folders  
- ✅ Optional CLI for automation  
- ✅ Supports JPEG, JPG, PNG, NEF, CR2, RAW formats

---

> Note: The GUI (UI.py) and screenshot assets referenced in earlier versions are not present in this repository. This README reflects the current CLI-only implementation.

---

## 🚀 Installation

1. Clone or download this repo:

    `git clone https://github.com/aravindhms/PhotoSort.git`  
    `cd PhotoSort`

2. Install dependencies:

    `pip install -r requirements.txt`

---

## 🖥️ Usage

Run the command-line tool:

    python main.py -s <source_path> -d <destination_path> -t <copy|move> -f <YM|YMD>

**Example:**

    python main.py -s "E:/Camera/Unsorted" -d "E:/Camera/Sorted" -t copy -f YMD

This will scan the source folder for supported image files, determine the capture date (EXIF) or fallback to file modification time, and copy or move files into `Year/Month` (YM) or `Year/Month/Day` (YMD) folders under the destination.

---

## 📁 Folder Structure

    PhotoSort/
    ├── photosort.py          # Core logic
    ├── main.py               # CLI entry point
    ├── requirements.txt      # Dependencies
    ├── README.md             # This file

(Older references to `UI.py` and `Screenshots/` have been removed from this repository.)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License
