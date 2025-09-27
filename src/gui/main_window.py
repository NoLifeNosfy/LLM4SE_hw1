import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import TkinterDnD
from gui.import_frame import ImportFrame
from gui.export_settings_frame import ExportSettingsFrame
from gui.watermark_list_frame import WatermarkListFrame
from gui.preview_frame import PreviewFrame
from gui.watermark_edit_frame import WatermarkEditFrame
from file_io.file_handler import export_images

# Add the src directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class MainWindow(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Watermark Tool")
        self.geometry("1600x800")

        # --- Main Layout --- #
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_columnconfigure(0, weight=0, minsize=300)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # --- Preview Area (Middle) --- #
        self.preview_frame = PreviewFrame(main_frame)
        self.preview_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)

        # --- Image Import Area (Top-Left) --- #
        self.import_frame = ImportFrame(main_frame, on_image_select_callback=self.preview_frame.display_image)
        self.import_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

        # --- Watermark List Area (Bottom-Left) --- #
        self.watermark_list_frame = WatermarkListFrame(main_frame)
        self.watermark_list_frame.grid(row=1, column=0, sticky="ns", padx=5, pady=5)

        # --- Watermark Edit Area (Right) --- #
        self.watermark_edit_frame = WatermarkEditFrame(main_frame, self.preview_frame)
        self.watermark_edit_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # Set the callback for drag-and-drop communication
        self.preview_frame.on_watermark_drag_callback = self.watermark_edit_frame.on_watermark_drag

        # --- Action Button --- #
        export_button = ttk.Button(main_frame, text="Export All Images", command=self.open_export_settings)
        export_button.grid(row=1, column=2, sticky="se", padx=5, pady=5)

    def open_export_settings(self):
        ExportDialog(self)

class ExportDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.title("Export Settings")
        self.parent = parent
        self.grab_set()

        self.export_settings_frame = ExportSettingsFrame(self)
        self.export_settings_frame.pack(padx=10, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill=tk.X)

        export_button = ttk.Button(button_frame, text="Export", command=self.export_images)
        export_button.pack(side=tk.RIGHT, padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT)

    def export_images(self):
        settings = self.export_settings_frame.get_settings()
        output_dir = settings["output_dir"]
        imported_files = self.parent.import_frame.get_imported_files()

        if not imported_files:
            messagebox.showwarning("No Files", "Please import images before exporting.", parent=self)
            return

        if not output_dir:
            messagebox.showwarning("No Output Directory", "Please select an output directory.", parent=self)
            return

        try:
            scale_width = int(settings["scale_width"]) if settings["scale_width"] else None
            scale_height = int(settings["scale_height"]) if settings["scale_height"] else None
        except ValueError:
            messagebox.showerror("Invalid Scale", "Please enter valid integers for scaling.", parent=self)
            return

        export_images(
            image_paths=imported_files,
            output_dir=output_dir,
            prefix=settings["prefix"],
            suffix=settings["suffix"],
            scale_width=scale_width,
            scale_height=scale_height,
            jpeg_quality=settings["jpeg_quality"]
        )

        messagebox.showinfo("Export Complete", f"Exported {len(imported_files)} images to \n{output_dir}", parent=self)
        self.destroy()
