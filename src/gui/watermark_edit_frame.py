# This file will contain the UI for the watermark editor section.
import tkinter as tk
from tkinter import ttk
from PIL import Image
from gui.text_watermark_frame import TextWatermarkFrame
from watermarking.watermark import apply_text_watermark

class WatermarkEditFrame(ttk.LabelFrame):
    def __init__(self, parent, preview_frame):
        super().__init__(parent, text="Watermark Editor", padding="10")
        self.preview_frame = preview_frame

        # --- Main Layout ---
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # --- Tabbed Notebook ---
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # --- Text Watermark Tab ---
        text_watermark_tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(text_watermark_tab_frame, text="Text Watermark")
        
        self.text_watermark_frame = TextWatermarkFrame(text_watermark_tab_frame)
        self.text_watermark_frame.pack(fill=tk.BOTH, expand=True)

        # --- Image Watermark Tab ---
        image_watermark_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(image_watermark_frame, text="Image Watermark")
        ttk.Label(image_watermark_frame, text="Image-specific watermark settings placeholder.").pack()

        # --- Common Settings Area ---
        common_settings_frame = ttk.LabelFrame(self, text="Common Settings", padding="10")
        common_settings_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        # Create a frame for the 9-grid layout
        grid_layout_frame = ttk.Frame(common_settings_frame)
        grid_layout_frame.pack(pady=5)

        # Create and place the 9 buttons in a 3x3 grid
        positions = [
            ("Top-Left", 0, 0), ("Top-Center", 0, 1), ("Top-Right", 0, 2),
            ("Middle-Left", 1, 0), ("Center", 1, 1), ("Middle-Right", 1, 2),
            ("Bottom-Left", 2, 0), ("Bottom-Center", 2, 1), ("Bottom-Right", 2, 2)
        ]

        self.position_var = tk.StringVar(value="Center")
        for text, row, col in positions:
            button = ttk.Button(grid_layout_frame, text=text, width=12, command=lambda t=text: self.position_var.set(t))
            button.grid(row=row, column=col, padx=2, pady=2)

        # --- Opacity and Rotation Settings ---
        opacity_rotation_frame = ttk.Frame(common_settings_frame)
        opacity_rotation_frame.pack(pady=10, fill=tk.X, expand=True)

        # Opacity
        opacity_label = ttk.Label(opacity_rotation_frame, text="Opacity:")
        opacity_label.pack(side=tk.LEFT, padx=(0, 5))

        self.opacity_var = tk.DoubleVar(value=1.0)
        opacity_scale = ttk.Scale(opacity_rotation_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=self.opacity_var)
        opacity_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Rotation
        rotation_label = ttk.Label(opacity_rotation_frame, text="Rotation:")
        rotation_label.pack(side=tk.LEFT, padx=(20, 5))

        self.rotation_var = tk.IntVar(value=0)
        rotation_spinbox = ttk.Spinbox(opacity_rotation_frame, from_=0, to=360, increment=1, textvariable=self.rotation_var, width=5)
        rotation_spinbox.pack(side=tk.LEFT)

        # --- Action Buttons ---
        action_buttons_frame = ttk.Frame(common_settings_frame)
        action_buttons_frame.pack(pady=10, fill=tk.X, expand=True)

        add_button = ttk.Button(action_buttons_frame, text="Add Watermark")
        add_button.pack(side=tk.RIGHT, padx=5)

        confirm_button = ttk.Button(action_buttons_frame, text="Confirm", command=self.apply_watermark)
        confirm_button.pack(side=tk.RIGHT)

    def apply_watermark(self):
        if not self.preview_frame.original_image:
            return

        settings = self.text_watermark_frame.get_settings()
        
        # Add common settings
        settings["opacity"] = self.opacity_var.get()
        settings["rotation"] = self.rotation_var.get()
        settings["position"] = self.position_var.get()

        # 使用原始图像应用水印，而不是当前显示的图像
        # 这样可以确保每次都是在原始图像上添加水印，而不是叠加
        watermarked_image = apply_text_watermark(self.preview_frame.original_image.copy(), settings)
        
        if watermarked_image:
            # 更新预览显示，但保留原始图像不变
            self.preview_frame.update_image_display(watermarked_image)
