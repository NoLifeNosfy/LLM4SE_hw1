# This file will contain the UI for the preview section.
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class PreviewFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Preview", padding="10")
        self.image_path = None
        self.original_image = None
        self.displayed_image = None
        self.image_id = None

        self.canvas = tk.Canvas(self, background="lightgrey", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.on_resize)

    def display_image(self, image_path):
        if not image_path:
            self.clear_preview()
            return

        self.image_path = image_path
        try:
            self.original_image = Image.open(image_path)
            self.update_image_display()
        except Exception as e:
            print(f"Error opening image {image_path}: {e}")
            self.clear_preview()

    def update_image_display(self):
        if not self.original_image:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1: # Canvas not yet sized
            return

        img_copy = self.original_image.copy()
        img_copy.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)

        self.displayed_image = ImageTk.PhotoImage(img_copy)

        if self.image_id:
            self.canvas.delete(self.image_id)

        self.image_id = self.canvas.create_image(
            canvas_width / 2,
            canvas_height / 2,
            anchor=tk.CENTER,
            image=self.displayed_image
        )

    def on_resize(self, event):
        self.update_image_display()

    def clear_preview(self):
        if self.image_id:
            self.canvas.delete(self.image_id)
        self.image_path = None
        self.original_image = None
        self.displayed_image = None
        self.image_id = None