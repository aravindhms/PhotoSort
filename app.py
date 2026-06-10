import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from sorter import sort_photos_generator, undo_last_sort_generator, HISTORY_FILE, SUPPORTED_FORMATS

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class PhotoSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PhotoSort")
        self.geometry("900x650")
        self.resizable(False, False)

        # Variables
        self.source_folder = ctk.StringVar()
        self.destination_folder = ctk.StringVar()
        self.folder_structure = ctk.StringVar(value="Year / Month")
        self.process_type = ctk.StringVar(value="Copy")
        self.custom_prefix = ctk.StringVar(value="")
        self.dry_run = ctk.BooleanVar(value=False)

        # Grid Layout (1 row, 2 columns)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.build_sidebar()
        self.build_main_area()

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)

        # Branding
        ctk.CTkLabel(self.sidebar, text="📸 PhotoSort", font=ctk.CTkFont(size=30, weight="bold")).grid(row=0, column=0, padx=20, pady=(40, 5))
        ctk.CTkLabel(self.sidebar, text="Organize your memories.", font=ctk.CTkFont(size=13), text_color="gray").grid(row=1, column=0, padx=20, pady=(0, 10))

        # Supported Formats
        formats_str = "Formats: " + ", ".join(sorted([f.replace('.', '').upper() for f in SUPPORTED_FORMATS]))
        ctk.CTkLabel(self.sidebar, text=formats_str, font=ctk.CTkFont(size=11), text_color="gray", wraplength=240).grid(row=2, column=0, padx=20, pady=(0, 20))

        # Start Button
        self.start_btn = ctk.CTkButton(self.sidebar, text="✨ START SORTING", font=ctk.CTkFont(size=18, weight="bold"), height=55, corner_radius=10, command=self.start_sorting)
        self.start_btn.grid(row=3, column=0, padx=30, pady=20, sticky="ew")

        # Progress Area
        self.progress_bar = ctk.CTkProgressBar(self.sidebar, height=12)
        self.progress_bar.grid(row=4, column=0, padx=30, pady=(10, 5), sticky="ew")
        self.progress_bar.set(0)
        self.progress_bar.grid_remove() # Hide initially

        self.status_label = ctk.CTkLabel(self.sidebar, text="", font=ctk.CTkFont(size=12), wraplength=220)
        self.status_label.grid(row=5, column=0, padx=30, pady=0, sticky="n")

        # Undo Button
        self.undo_btn = ctk.CTkButton(self.sidebar, text="↩️ Undo Last Sort", fg_color="#c0392b", hover_color="#e74c3c", command=self.undo_sort)
        self.undo_btn.grid(row=6, column=0, padx=30, pady=(30, 20), sticky="ew")
        self.check_undo_availability()

        # Footer
        ctk.CTkLabel(self.sidebar, text="© PhotoSort by Aravindh", font=ctk.CTkFont(size=10), text_color="gray").grid(row=7, column=0, pady=(0, 10), sticky="s")

    def check_undo_availability(self):
        if os.path.exists(HISTORY_FILE):
            self.undo_btn.configure(state="normal")
        else:
            self.undo_btn.configure(state="disabled")

    def build_main_area(self):
        self.main_area = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_columnconfigure(0, weight=1)

        # --- Card 1: Locations ---
        card1 = ctk.CTkFrame(self.main_area, corner_radius=15)
        card1.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        card1.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(card1, text="📁 Locations", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=25, pady=(20, 15))

        # Source
        ctk.CTkButton(card1, text="Browse Source", width=120, height=35, command=self.browse_source, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=1, column=0, padx=(25, 10), pady=(0, 15))
        ctk.CTkEntry(card1, textvariable=self.source_folder, placeholder_text="Select photos folder...", height=35).grid(row=1, column=1, padx=(0, 25), pady=(0, 15), sticky="ew")

        # Destination
        ctk.CTkButton(card1, text="Browse Dest", width=120, height=35, command=self.browse_dest, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=2, column=0, padx=(25, 10), pady=(0, 25))
        ctk.CTkEntry(card1, textvariable=self.destination_folder, placeholder_text="Select destination folder...", height=35).grid(row=2, column=1, padx=(0, 25), pady=(0, 25), sticky="ew")

        # --- Card 2: Sorting Options ---
        card2 = ctk.CTkFrame(self.main_area, corner_radius=15)
        card2.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        card2.grid_columnconfigure(0, weight=1)
        card2.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(card2, text="⚙️ Sorting Settings", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=25, pady=(20, 15))

        # Structure OptionMenu
        ctk.CTkLabel(card2, text="Folder Structure:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, sticky="w", padx=25)
        
        structure_options = [
            "Year Only", 
            "Year / Month", 
            "Year / Month / Day", 
            "Year / Month Name", 
            "By File Extension", 
            "Year / File Extension", 
            "Flat Directory (No Subfolders)"
        ]
        self.struct_menu = ctk.CTkOptionMenu(card2, values=structure_options, variable=self.folder_structure)
        self.struct_menu.grid(row=2, column=0, sticky="ew", padx=(25, 10), pady=(5, 15))

        # Process Segmented Button
        ctk.CTkLabel(card2, text="Process Type:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=1, sticky="w", padx=(10, 25))
        self.seg_process = ctk.CTkSegmentedButton(card2, values=["Copy", "Move"], variable=self.process_type)
        self.seg_process.grid(row=2, column=1, sticky="ew", padx=(10, 25), pady=(5, 15))

        # Dry Run Switch
        self.dry_switch = ctk.CTkSwitch(card2, text="Dry Run (Simulation Mode)", variable=self.dry_run, font=ctk.CTkFont(weight="bold"))
        self.dry_switch.grid(row=3, column=0, columnspan=2, sticky="w", padx=25, pady=(5, 25))

        # --- Card 3: Advanced ---
        card3 = ctk.CTkFrame(self.main_area, corner_radius=15)
        card3.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        card3.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card3, text="🛠️ Advanced", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, sticky="w", padx=25, pady=(20, 10))
        
        ctk.CTkLabel(card3, text="Custom Naming Prefix:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, sticky="w", padx=25)
        ctk.CTkEntry(card3, textvariable=self.custom_prefix, placeholder_text="e.g. Vacation (Optional)", height=35).grid(row=2, column=0, sticky="ew", padx=25, pady=(5, 25))

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder: self.source_folder.set(folder)

    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder: self.destination_folder.set(folder)

    def start_sorting(self):
        src = self.source_folder.get()
        dest = self.destination_folder.get()
        if not src or not dest:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return

        self.start_btn.configure(state="disabled", text="PROCESSING...")
        self.undo_btn.configure(state="disabled")
        self.progress_bar.grid()
        self.progress_bar.set(0)
        
        if self.dry_run.get():
            self.status_label.configure(text="[SIMULATION] Scanning files...", text_color="yellow")
        else:
            self.status_label.configure(text="Scanning files...", text_color="white")

        threading.Thread(target=self.run_sort_task, args=(src, dest), daemon=True).start()

    def run_sort_task(self, src, dest):
        struct_map = {
            "Year Only": "Y",
            "Year / Month": "YM",
            "Year / Month / Day": "YMD",
            "Year / Month Name": "YMN",
            "By File Extension": "EXT",
            "Year / File Extension": "YEXT",
            "Flat Directory (No Subfolders)": "FLAT"
        }
        struct_val = struct_map.get(self.folder_structure.get(), "YM")
        ptype_val = "copy" if self.process_type.get() == "Copy" else "move"
        prefix = self.custom_prefix.get().strip()
        is_dry = self.dry_run.get()
        
        generator = sort_photos_generator(src, dest, ptype_val, struct_val, prefix, is_dry)
        for update in generator:
            self.after(0, self.update_ui, update, is_dry)

    def undo_sort(self):
        if not messagebox.askyesno("Confirm Undo", "Are you sure you want to undo the last sort operation?"):
            return
            
        self.start_btn.configure(state="disabled")
        self.undo_btn.configure(state="disabled", text="UNDOING...")
        self.progress_bar.grid()
        self.progress_bar.set(0)
        self.status_label.configure(text="Starting Undo...", text_color="white")
        
        threading.Thread(target=self.run_undo_task, daemon=True).start()

    def run_undo_task(self):
        generator = undo_last_sort_generator()
        for update in generator:
            self.after(0, self.update_undo_ui, update)

    def update_undo_ui(self, data):
        status = data.get("status")
        
        if status == "start":
            self.status_label.configure(text=f"Reversing {data['total']} operations...")
            
        elif status == "progress":
            current = data["current"]
            total = data["total"]
            self.progress_bar.set(current / total if total > 0 else 0)
            self.status_label.configure(text=f"Undoing: {current} / {total}\n{data['file']}")
            
        elif status == "done":
            self.start_btn.configure(state="normal", text="✨ START SORTING")
            self.undo_btn.configure(text="↩️ Undo Last Sort")
            self.check_undo_availability()
            
            total = data["total"]
            success = data["success"]
            errors = data["errors"]
            
            if total == 0:
                 self.status_label.configure(text=data.get("msg", "Nothing to undo."), text_color="white")
            elif errors > 0:
                self.status_label.configure(text=f"Undo completed with errors.\nTotal: {total}\nSuccess: {success}\nErrors: {errors}", text_color="orange")
            else:
                self.status_label.configure(text=f"Successfully undid {success} operations!", text_color="#2ecc71")

    def update_ui(self, data, is_dry):
        status = data.get("status")
        
        prefix_txt = "[SIMULATION] " if is_dry else ""
        
        if status == "start":
            self.status_label.configure(text=f"{prefix_txt}Found {data['total']} files. Starting...")
            
        elif status == "progress":
            current = data["current"]
            total = data["total"]
            self.progress_bar.set(current / total if total > 0 else 0)
            self.status_label.configure(text=f"{prefix_txt}Processing: {current} / {total}\n{data['file']}")
            
        elif status == "done":
            self.start_btn.configure(state="normal", text="✨ START SORTING")
            self.check_undo_availability()
            
            total = data["total"]
            success = data["success"]
            errors = data["errors"]
            
            if errors > 0:
                self.status_label.configure(text=f"{prefix_txt}Completed with errors.\nTotal: {total}\nSuccess: {success}\nErrors: {errors}", text_color="orange")
            else:
                self.status_label.configure(text=f"{prefix_txt}Successfully sorted {success} files!", text_color="#2ecc71")

if __name__ == "__main__":
    app = PhotoSorterApp()
    app.mainloop()
