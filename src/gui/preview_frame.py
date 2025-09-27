import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class PreviewFrame(ttk.LabelFrame):
    def __init__(self, parent, on_watermark_drag_callback=None):
        super().__init__(parent, text="Preview", padding="10")
        self.on_watermark_drag_callback = on_watermark_drag_callback

        # Image attributes
        self.original_image = None
        self.displayed_bg_image_tk = None
        self.bg_image_id = None

        # Watermark attributes
        self.watermark_layer = None
        self.watermark_tk = None
        self.watermark_id = None
        self.watermark_pos = {"x": 0, "y": 0}

        # Dragging attributes
        self._drag_data = {"x": 0, "y": 0, "item": None}

        self.canvas = tk.Canvas(self, background="lightgrey", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.tag_bind("watermark", "<ButtonPress-1>", self._on_press)
        self.canvas.tag_bind("watermark", "<B1-Motion>", self._on_drag)
        self.canvas.tag_bind("watermark", "<ButtonRelease-1>", self._on_release)

    def display_image(self, image_source):
        self.clear_preview()
        if isinstance(image_source, str):
            try:
                self.original_image = Image.open(image_source)
            except Exception as e:
                print(f"Error opening image {image_source}: {e}")
                self.original_image = None
        elif isinstance(image_source, Image.Image):
            self.original_image = image_source
        
        self._update_bg_image_display()

    def _update_bg_image_display(self):
        if self.bg_image_id:
            self.canvas.delete(self.bg_image_id)

        if not self.original_image:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1: return

        img_copy = self.original_image.copy()
        img_copy.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        self.displayed_bg_image_tk = ImageTk.PhotoImage(img_copy)

        self.bg_image_id = self.canvas.create_image(
            canvas_width / 2, canvas_height / 2, 
            anchor=tk.CENTER, image=self.displayed_bg_image_tk
        )
        self.canvas.lower(self.bg_image_id) # Ensure background is always at the bottom

    def draw_watermark(self, watermark_layer, position="Center"):
        self.clear_watermark()
        if not watermark_layer or not self.original_image:
            return

        self.watermark_layer = watermark_layer
        self.watermark_tk = ImageTk.PhotoImage(self.watermark_layer)
        
        img_w, img_h = self.original_image.size
        wm_w, wm_h = self.watermark_layer.size

        # Calculate initial position based on string
        if isinstance(position, str):
            if "Left" in position:
                x = 10
            elif "Right" in position:
                x = img_w - wm_w - 10
            else: # Center
                x = (img_w - wm_w) // 2
            
            if "Top" in position:
                y = 10
            elif "Bottom" in position:
                y = img_h - wm_h - 10
            else: # Middle or Center
                y = (img_h - wm_h) // 2
        else: # Assume position is a dict {x, y}
            x, y = position.get("x", 0), position.get("y", 0)

        self.watermark_pos = {"x": x, "y": y}

        self.watermark_id = self.canvas.create_image(x, y, anchor=tk.NW, image=self.watermark_tk, tags=("watermark",))
        self._update_watermark_display()

    def _update_watermark_display(self):
        if not self.watermark_id or not self.original_image:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1: return

        scale_x = canvas_width / self.original_image.width
        scale_y = canvas_height / self.original_image.height
        scale = min(scale_x, scale_y)

        # Calculate the scaled image dimensions and offset on the canvas
        scaled_w = int(self.original_image.width * scale)
        scaled_h = int(self.original_image.height * scale)
        offset_x = (canvas_width - scaled_w) / 2
        offset_y = (canvas_height - scaled_h) / 2

        # Move watermark according to the background image's scale and offset
        new_x = offset_x + (self.watermark_pos["x"] * scale)
        new_y = offset_y + (self.watermark_pos["y"] * scale)
        
        self.canvas.coords(self.watermark_id, new_x, new_y)

    def clear_watermark(self):
        if self.watermark_id:
            self.canvas.delete(self.watermark_id)
        self.watermark_layer = None
        self.watermark_tk = None
        self.watermark_id = None
        self.watermark_pos = {"x": 0, "y": 0}

    def clear_preview(self):
        self.clear_watermark()
        if self.bg_image_id:
            self.canvas.delete(self.bg_image_id)
        self.original_image = None
        self.displayed_bg_image_tk = None
        self.bg_image_id = None

    def _on_resize(self, event):
        self._update_bg_image_display()
        self._update_watermark_display()

    def _on_press(self, event):
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _on_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.canvas.move(self._drag_data["item"], dx, dy)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _on_release(self, event):
        if not self.original_image: return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        scale_x = canvas_width / self.original_image.width
        scale_y = canvas_height / self.original_image.height
        scale = min(scale_x, scale_y)

        scaled_w = int(self.original_image.width * scale)
        scaled_h = int(self.original_image.height * scale)
        offset_x = (canvas_width - scaled_w) / 2
        offset_y = (canvas_height - scaled_h) / 2

        # Convert canvas coords back to original image coords
        canvas_x, canvas_y = self.canvas.coords(self.watermark_id)
        original_x = int((canvas_x - offset_x) / scale)
        original_y = int((canvas_y - offset_y) / scale)

        self.watermark_pos = {"x": original_x, "y": original_y}
        self._drag_data["item"] = None

        if self.on_watermark_drag_callback:
            self.on_watermark_drag_callback(self.watermark_pos)
