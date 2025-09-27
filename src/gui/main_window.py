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
from config import template_manager

# Add the src directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class MainWindow(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Watermark Tool")
        self.geometry("1600x1000")
        self.templates_data = {}

        # --- Main Layout --- #
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_columnconfigure(0, weight=0, minsize=300)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # --- UI Frames Initialization --- #
        self.watermark_edit_frame = WatermarkEditFrame(main_frame, None)
        self.watermark_edit_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.preview_frame = PreviewFrame(main_frame, on_watermark_drag_callback=self.watermark_edit_frame.on_watermark_drag)
        self.preview_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
        
        self.watermark_edit_frame.preview_frame = self.preview_frame

        self.import_frame = ImportFrame(main_frame, on_image_select_callback=self.preview_frame.display_image)
        self.import_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

        self.watermark_list_frame = WatermarkListFrame(
            main_frame,
            on_load_callback=self.handle_load_template,
            on_save_callback=self.handle_save_template,
            on_delete_callback=self.handle_delete_template
        )
        self.watermark_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        export_button = ttk.Button(main_frame, text="Export All Images", command=self.open_export_settings)
        export_button.grid(row=1, column=2, sticky="se", padx=5, pady=5)

        # --- Load Templates and Set initial state --- #
        self._load_and_apply_templates()

        # --- Handle window closing --- #
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _load_and_apply_templates(self):
        """Loads all templates and applies the last used one."""
        self.templates_data = template_manager.load_templates()
        self.watermark_list_frame.update_template_list(self.templates_data.get("templates", {}))
        
        last_used_name = self.templates_data.get("__metadata__", {}).get("last_used")
        if last_used_name and last_used_name in self.templates_data.get("templates", {}):
            self.watermark_edit_frame.set_settings(self.templates_data["templates"][last_used_name])

    def handle_save_template(self, template_name):
        """Saves the current settings as a new template."""
        if template_name in self.templates_data.get("templates", {}):
            if not messagebox.askyesno("Overwrite Template", f"Template '{template_name}' already exists. Overwrite it?", parent=self):
                return
        
        current_settings = self.watermark_edit_frame.get_current_settings()
        if "templates" not in self.templates_data:
            self.templates_data["templates"] = {}
        self.templates_data["templates"][template_name] = current_settings
        
        template_manager.save_templates(self.templates_data)
        self.watermark_list_frame.update_template_list(self.templates_data["templates"])
        messagebox.showinfo("Template Saved", f"Template '{template_name}' was saved.", parent=self)

    def handle_load_template(self):
        """Loads the selected template from the list."""
        template_name = self.watermark_list_frame.get_selected_template()
        if not template_name:
            messagebox.showwarning("No Selection", "Please select a template to load.", parent=self)
            return
            
        template_settings = self.templates_data.get("templates", {}).get(template_name)
        if template_settings:
            self.watermark_edit_frame.set_settings(template_settings)
        else:
            messagebox.showerror("Error", f"Could not find template '{template_name}'.", parent=self)

    def handle_delete_template(self):
        """Deletes the selected template from the list."""
        template_name = self.watermark_list_frame.get_selected_template()
        if not template_name:
            messagebox.showwarning("No Selection", "Please select a template to delete.", parent=self)
            return

        if messagebox.askyesno("Delete Template", f"Are you sure you want to delete '{template_name}'?", parent=self):
            if "templates" in self.templates_data and template_name in self.templates_data["templates"]:
                del self.templates_data["templates"][template_name]
                template_manager.save_templates(self.templates_data)
                self.watermark_list_frame.update_template_list(self.templates_data["templates"])
                messagebox.showinfo("Template Deleted", f"Template '{template_name}' was deleted.", parent=self)

    def _on_closing(self):
        """Handles saving the last used template on application exit."""
        current_settings = self.watermark_edit_frame.get_current_settings()
        # A simple way to identify a "valid" setting is if it has a type
        if current_settings.get("type"):
            template_name = self.watermark_list_frame.get_selected_template() or "Last Session"
            if "templates" not in self.templates_data:
                self.templates_data["templates"] = {}
            self.templates_data["templates"][template_name] = current_settings
            if "__metadata__" not in self.templates_data:
                self.templates_data["__metadata__"] = {}
            self.templates_data["__metadata__"]["last_used"] = template_name
            template_manager.save_templates(self.templates_data)
        
        self.destroy()

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

        # Get the final watermark settings from the edit frame for the export
        watermark_settings = self.parent.watermark_edit_frame.get_current_settings()

        export_images(
            image_paths=imported_files,
            output_dir=output_dir,
            watermark_settings=watermark_settings,
            prefix=settings["prefix"],
            suffix=settings["suffix"],
            width_scale_ratio=settings["width_scale_ratio"],
            height_scale_ratio=settings["height_scale_ratio"],
            jpeg_quality=settings["jpeg_quality"]
        )

        messagebox.showinfo("Export Complete", f"Exported {len(imported_files)} images to \n{output_dir}", parent=self)
        self.destroy()