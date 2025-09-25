import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES
from file_io.file_handler import get_image_paths
import os

class ImportFrame(ttk.LabelFrame):
    def __init__(self, parent, on_image_select_callback=None):
        super().__init__(parent, text="Import Images", padding="10")
        self.on_image_select_callback = on_image_select_callback
        self.selected_image_path = None

        self.imported_files = []
        self.thumbnails = []

        # --- Main Layout --- #
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Scrollable Image List --- #
        canvas = tk.Canvas(main_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Drag and Drop Message --- #
        self.dnd_message_label = ttk.Label(
            canvas,
            text="Drag and drop image files or folders here",
            background='#f0f0f0',
            foreground='#a0a0a0',
            font=("Arial", 12)
        )
        self.dnd_message_label.place(relx=0.5, rely=0.5, anchor='center')

        # --- Drag and Drop Binding --- #
        canvas.drop_target_register(DND_FILES)
        canvas.dnd_bind('<<Drop>>', self.handle_drop)

        # Buttons for adding files/folders
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=5)

        add_files_button = ttk.Button(button_frame, text="Add File(s)", command=self.add_files)
        add_files_button.pack(side=tk.LEFT, padx=5)

        add_folder_button = ttk.Button(button_frame, text="Add Folder", command=self.add_folder)
        add_folder_button.pack(side=tk.LEFT, padx=5)

        self.update_image_list()

    def get_imported_files(self):
        return self.imported_files

    def add_image_paths(self, paths):
        """Adds a list of paths to the imported files list, avoiding duplicates."""
        added = False
        for path in paths:
            if path not in self.imported_files:
                self.imported_files.append(path)
                added = True
        
        if added:
            self.update_image_list()
            if self.imported_files and not self.selected_image_path:
                self.select_image(self.imported_files[0])

    def handle_drop(self, event):
        """Handles files dropped onto the canvas."""
        dropped_paths = self.tk.splitlist(event.data)
        paths_to_add = []
        for path in dropped_paths:
            paths_to_add.extend(list(get_image_paths(path, recursive=True)))
        self.add_image_paths(paths_to_add)

    def add_files(self):
        """Open file dialog to select and add multiple image files."""
        file_paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All Files", "*.*"),
            ]
        )
        if file_paths:
            self.add_image_paths(file_paths)

    def add_folder(self):
        """Open directory dialog to select and add a folder of images."""
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            image_paths = get_image_paths(folder_path, recursive=False)
            self.add_image_paths(image_paths)

    def remove_image(self, file_path):
        """Removes an image from the imported list."""
        if file_path in self.imported_files:
            current_index = self.imported_files.index(file_path)
            self.imported_files.remove(file_path)
            
            if file_path == self.selected_image_path:
                if self.imported_files:
                    new_index = min(current_index, len(self.imported_files) - 1)
                    self.select_image(self.imported_files[new_index])
                else:
                    self.select_image(None)
        
        self.update_image_list()

    def update_image_list(self):
        """Clears and repopulates the scrollable frame with image thumbnails and filenames."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.thumbnails.clear()

        if not self.imported_files:
            self.dnd_message_label.place(relx=0.5, rely=0.5, anchor='center')
        else:
            self.dnd_message_label.place_forget()

        for file_path in self.imported_files:
            try:
                item_frame = ttk.Frame(self.scrollable_frame, padding=5)
                item_frame.pack(fill=tk.X, expand=True)

                if file_path == self.selected_image_path:
                    style = ttk.Style()
                    style.configure("Selected.TFrame", background="#cce5ff")
                    item_frame.configure(style="Selected.TFrame")

                item_frame.columnconfigure(1, weight=1)

                img = Image.open(file_path)
                img.thumbnail((50, 50))
                thumb = ImageTk.PhotoImage(img)
                self.thumbnails.append(thumb)

                thumb_label = ttk.Label(item_frame, image=thumb)
                thumb_label.grid(row=0, column=0, padx=5, sticky='w')

                filename = os.path.basename(file_path)
                name_label = ttk.Label(item_frame, text=filename, anchor="w")
                name_label.grid(row=0, column=1, padx=5, sticky='ew')

                item_frame.bind("<Button-1>", lambda e, p=file_path: self.select_image(p))
                thumb_label.bind("<Button-1>", lambda e, p=file_path: self.select_image(p))
                name_label.bind("<Button-1>", lambda e, p=file_path: self.select_image(p))

                remove_button = ttk.Button(
                    item_frame,
                    text="Remove",
                    command=lambda p=file_path: self.remove_image(p)
                )
                remove_button.grid(row=0, column=2, padx=5, sticky='e')

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    def select_image(self, file_path):
        self.selected_image_path = file_path
        if self.on_image_select_callback:
            self.on_image_select_callback(file_path)
        self.update_image_list()
