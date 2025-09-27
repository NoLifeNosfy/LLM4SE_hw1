import tkinter as tk
from tkinter import ttk
from gui.text_watermark_frame import TextWatermarkFrame
from gui.image_watermark_frame import ImageWatermarkFrame
from watermarking.watermark import create_text_watermark_layer, create_image_watermark_layer

class WatermarkEditFrame(ttk.LabelFrame):
    def __init__(self, parent, preview_frame):
        super().__init__(parent, text="Watermark Editor", padding="10")
        self.preview_frame = preview_frame
        self.watermark_settings = {"position": "Center"} # Holds the live settings

        # --- Main Layout ---
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # --- Tabbed Notebook ---
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # --- Text Watermark Tab ---
        text_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(text_tab, text="Text Watermark")
        self.text_watermark_frame = TextWatermarkFrame(text_tab)
        self.text_watermark_frame.pack(fill=tk.BOTH, expand=True)

        # --- Image Watermark Tab ---
        image_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(image_tab, text="Image Watermark")
        self.image_watermark_frame = ImageWatermarkFrame(image_tab)
        self.image_watermark_frame.pack(fill=tk.BOTH, expand=True)

        # --- Common Settings Area ---
        common_settings = ttk.LabelFrame(self, text="Common Settings", padding="10")
        common_settings.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        # Position Grid
        grid_layout = ttk.Frame(common_settings)
        grid_layout.pack(pady=5)
        self.position_var = tk.StringVar(value="Center")
        positions = [
            ("Top-Left", 0, 0), ("Top-Center", 0, 1), ("Top-Right", 0, 2),
            ("Middle-Left", 1, 0), ("Center", 1, 1), ("Middle-Right", 1, 2),
            ("Bottom-Left", 2, 0), ("Bottom-Center", 2, 1), ("Bottom-Right", 2, 2)
        ]
        for text, row, col in positions:
            btn = ttk.Button(grid_layout, text=text, width=12, 
                           command=lambda t=text: self._set_position(t))
            btn.grid(row=row, column=col, padx=2, pady=2)

        # Opacity and Rotation
        opacity_rotation_frame = ttk.Frame(common_settings)
        opacity_rotation_frame.pack(pady=10, fill=tk.X, expand=True)
        ttk.Label(opacity_rotation_frame, text="Opacity:").pack(side=tk.LEFT, padx=(0, 5))
        self.opacity_var = tk.IntVar(value=100)
        ttk.Scale(opacity_rotation_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.opacity_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(opacity_rotation_frame, text="Rotation:").pack(side=tk.LEFT, padx=(20, 5))
        self.rotation_var = tk.IntVar(value=0)
        ttk.Spinbox(opacity_rotation_frame, from_=0, to=360, increment=1, textvariable=self.rotation_var, width=5).pack(side=tk.LEFT)

        # --- Action Buttons ---
        action_buttons = ttk.Frame(self)
        action_buttons.grid(row=2, column=0, sticky="e", pady=(10,0))
        ttk.Button(action_buttons, text="Update Preview", command=self.update_watermark_preview).pack(side=tk.RIGHT, padx=5)
        ttk.Button(action_buttons, text="Remove Watermark", command=self.preview_frame.clear_watermark).pack(side=tk.RIGHT)

    def _set_position(self, pos_string):
        self.position_var.set(pos_string)
        self.watermark_settings['position'] = pos_string
        # Remove custom coordinates when a grid button is pressed
        self.watermark_settings.pop('x', None)
        self.watermark_settings.pop('y', None)
        self.update_watermark_preview()

    def on_watermark_drag(self, new_pos):
        """Callback for when the watermark is dragged in the preview frame."""
        self.position_var.set("Custom") # Indicate manual positioning
        self.watermark_settings['x'] = new_pos['x']
        self.watermark_settings['y'] = new_pos['y']
        self.watermark_settings['position'] = "Custom"

    def update_watermark_preview(self):
        """Gathers all settings, creates a watermark layer, and tells the preview frame to draw it."""
        if not self.preview_frame.original_image:
            return

        # Gather common settings
        common_settings = {
            "opacity": self.opacity_var.get() / 100.0,
            "rotation": self.rotation_var.get(),
        }
        self.watermark_settings.update(common_settings)

        current_tab = self.notebook.index("current")
        watermark_layer = None

        if current_tab == 0: # Text watermark
            text_settings = self.text_watermark_frame.get_settings()
            self.watermark_settings.update(text_settings)
            watermark_layer = create_text_watermark_layer(self.watermark_settings)
        else: # Image watermark
            watermark_image = self.image_watermark_frame.get_watermark_image()
            if watermark_image:
                watermark_layer = create_image_watermark_layer(watermark_image.copy(), self.watermark_settings)

        if watermark_layer:
            position = self.watermark_settings.get('position', 'Center')
            if position == 'Custom':
                position = {'x': self.watermark_settings.get('x'), 'y': self.watermark_settings.get('y')}
            self.preview_frame.draw_watermark(watermark_layer, position)