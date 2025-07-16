import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from photosort import sort_photos, SUPPORTED_FORMATS

ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class PhotoSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Photo Sort")
        self.geometry("740x380")
        self.resizable(False, False)

        self.source_folder = ctk.StringVar()
        self.destination_folder = ctk.StringVar()
        self.folder_structure = ctk.StringVar(value="YM")
        self.process_type = ctk.StringVar(value="copy")

        self.build_ui()

    def build_ui(self):
        padding = {"padx": 10, "pady": 10}

        # Source Folder
        ctk.CTkLabel(self, text="Source Folder:").grid(row=0, column=0, sticky="e", **padding)
        ctk.CTkEntry(self, textvariable=self.source_folder, width=380).grid(row=0, column=1, **padding)
        ctk.CTkButton(self, text="Browse", command=self.browse_source).grid(row=0, column=2, **padding)

        # Destination Folder
        ctk.CTkLabel(self, text="Destination Folder:").grid(row=1, column=0, sticky="e", **padding)
        ctk.CTkEntry(self, textvariable=self.destination_folder, width=380).grid(row=1, column=1, **padding)
        ctk.CTkButton(self, text="Browse", command=self.browse_destination).grid(row=1, column=2, **padding)

        # Folder Structure
        ctk.CTkLabel(self, text="Folder Structure:").grid(row=2, column=0, sticky="e", **padding)
        structure_frame = ctk.CTkFrame(self, fg_color="transparent")
        structure_frame.grid(row=2, column=1, columnspan=2, sticky="w", **padding)
        ctk.CTkRadioButton(structure_frame, text="Year/Month (YM)", variable=self.folder_structure, value="YM").pack(side="left", padx=10)
        ctk.CTkRadioButton(structure_frame, text="Year/Month/Day (YMD)", variable=self.folder_structure, value="YMD").pack(side="left", padx=10)

        # Process Type
        ctk.CTkLabel(self, text="Process Type:").grid(row=3, column=0, sticky="e", **padding)
        process_frame = ctk.CTkFrame(self, fg_color="transparent")
        process_frame.grid(row=3, column=1, columnspan=2, sticky="w", **padding)
        ctk.CTkRadioButton(process_frame, text="Copy", variable=self.process_type, value="copy").pack(side="left", padx=10)
        ctk.CTkRadioButton(process_frame, text="Move", variable=self.process_type, value="move").pack(side="left", padx=10)

        # Supported Formats
        ctk.CTkLabel(self, text="Supported Formats:", text_color="gray").grid(row=4, column=0, sticky="ne", **padding)
        formats_label = ", ".join(SUPPORTED_FORMATS)
        ctk.CTkLabel(self, text=formats_label, wraplength=400, text_color="gray", justify="left").grid(row=4, column=1, columnspan=2, sticky="w", **padding)

        # Status
        self.status_label = ctk.CTkLabel(self, text="", text_color="blue")
        self.status_label.grid(row=5, column=0, columnspan=3, sticky="w", padx=20, pady=(0, 0))

        # Stats
        self.stats_label = ctk.CTkLabel(self, text="", justify="left")
        self.stats_label.grid(row=6, column=0, columnspan=3, sticky="w", padx=20)

        # Action Buttons
        ctk.CTkButton(self, text="Start Sorting", width=120, command=self.start_sorting).grid(row=7, column=1, pady=20)
        ctk.CTkButton(self, text="Exit", width=80, command=self.quit).grid(row=7, column=2)

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_folder.set(folder)

    def browse_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.destination_folder.set(folder)

    def start_sorting(self):
        src = self.source_folder.get()
        dest = self.destination_folder.get()
        folder_struct = self.folder_structure.get()
        process = self.process_type.get()

        if not src or not dest:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return

        if not os.path.exists(src):
            messagebox.showerror("Error", "Source folder does not exist.")
            return

        self.status_label.configure(text="Sorting in progress...", text_color="blue")
        self.stats_label.configure(text="")

        try:
            total, success, errors = sort_photos(src, dest, process_type=process, folder_struct=folder_struct)
            self.status_label.configure(text="Sorting completed successfully!", text_color="green")
            self.stats_label.configure(
                text=f"Total files scanned: {total}\nSuccessfully sorted: {success}\nErrors: {errors}",
                text_color="black"
            )
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", text_color="red")
            self.stats_label.configure(text="")

if __name__ == "__main__":
    app = PhotoSorterApp()
    app.mainloop()
