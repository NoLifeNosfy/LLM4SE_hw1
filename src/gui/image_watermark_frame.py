import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os

class ImageWatermarkFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        
        self.original_watermark_image = None
        self.watermark_preview_tk = None # Keep a reference

        # --- UI Elements ---
        select_image_frame = ttk.Frame(self)
        select_image_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(select_image_frame, text="选择水印图片:").pack(side=tk.LEFT, padx=(0, 10))
        self.image_path_var = tk.StringVar()
        ttk.Entry(select_image_frame, textvariable=self.image_path_var, width=30, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(select_image_frame, text="浏览...", command=self.browse_watermark_image).pack(side=tk.LEFT, padx=5)
        
        scale_frame = ttk.Frame(self)
        scale_frame.pack(fill=tk.X, pady=5)
        
        # Add a button to apply scale changes to the local preview
        ttk.Button(scale_frame, text="更新预览", command=self._update_local_preview).pack(side=tk.RIGHT, padx=5)

        width_scale_frame = ttk.Frame(scale_frame)
        width_scale_frame.pack(fill=tk.X, pady=2)
        ttk.Label(width_scale_frame, text="宽度缩放比例:").pack(side=tk.LEFT, padx=(0, 10))
        self.width_scale_var = tk.StringVar(value="1.0")
        self.width_scale_entry = ttk.Entry(width_scale_frame, textvariable=self.width_scale_var, width=10)
        self.width_scale_entry.pack(side=tk.LEFT)
        
        height_scale_frame = ttk.Frame(scale_frame)
        height_scale_frame.pack(fill=tk.X, pady=2)
        ttk.Label(height_scale_frame, text="高度缩放比例:").pack(side=tk.LEFT, padx=(0, 10))
        self.height_scale_var = tk.StringVar(value="1.0")
        self.height_scale_entry = ttk.Entry(height_scale_frame, textvariable=self.height_scale_var, width=10)
        self.height_scale_entry.pack(side=tk.LEFT)
        
        bind_ratio_frame = ttk.Frame(scale_frame)
        bind_ratio_frame.pack(fill=tk.X, pady=2)
        self.bind_ratio_var = tk.BooleanVar(value=True)
        self.bind_ratio_check = ttk.Checkbutton(bind_ratio_frame, text="绑定长宽比", variable=self.bind_ratio_var)
        self.bind_ratio_check.pack(side=tk.LEFT)
        
        # --- Preview Area ---
        preview_container = ttk.LabelFrame(self, text="水印预览 (左上角200x200裁剪)", padding=5)
        preview_container.pack(pady=10)

        self.preview_canvas = tk.Canvas(preview_container, width=200, height=200, bg="lightgrey", highlightthickness=0)
        self.preview_canvas.pack()

        self.width_scale_var.trace_add("write", self._on_width_scale_change)
    
    def browse_watermark_image(self):
        file_path = filedialog.askopenfilename(title="选择水印图片", filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            self.image_path_var.set(file_path)
            try:
                self.original_watermark_image = Image.open(file_path).convert("RGBA")
                self._update_local_preview()
            except Exception as e:
                print(f"加载图片时出错: {e}")
                self.original_watermark_image = None
                self._update_local_preview()

    def _on_width_scale_change(self, *args):
        if self.bind_ratio_var.get():
            try:
                width_scale = float(self.width_scale_var.get())
                self.height_scale_var.set(f"{width_scale:.2f}")
            except (ValueError, tk.TclError):
                pass

    def _update_local_preview(self):
        self.preview_canvas.delete("all")
        if not self.original_watermark_image:
            return

        try:
            width_scale = float(self.width_scale_var.get())
            height_scale = float(self.height_scale_var.get())
        except ValueError:
            width_scale, height_scale = 1.0, 1.0

        if width_scale <= 0 or height_scale <= 0:
            return

        orig_width, orig_height = self.original_watermark_image.size
        new_width = int(orig_width * width_scale)
        new_height = int(orig_height * height_scale)

        if new_width > 0 and new_height > 0:
            scaled_image = self.original_watermark_image.resize((new_width, new_height), Image.LANCZOS)
            cropped_image = scaled_image.crop((0, 0, 200, 200))
            
            self.watermark_preview_tk = ImageTk.PhotoImage(cropped_image)
            self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.watermark_preview_tk)

    def set_settings(self, settings):
        image_path = settings.get("image_path", "")
        self.image_path_var.set(image_path)
        
        if image_path and os.path.exists(image_path):
            self.original_watermark_image = Image.open(image_path).convert("RGBA")
            self.width_scale_var.set(str(settings.get("width_scale", 1.0)))
            self.height_scale_var.set(str(settings.get("height_scale", 1.0)))
            self.bind_ratio_var.set(settings.get("bind_ratio", True))
            self._update_local_preview()
        else:
            self.original_watermark_image = None
            self._update_local_preview()

    def get_settings(self):
        try:
            width_scale = float(self.width_scale_var.get())
        except ValueError:
            width_scale = 1.0
        try:
            height_scale = float(self.height_scale_var.get())
        except ValueError:
            height_scale = 1.0
        return {
            "image_path": self.image_path_var.get(),
            "width_scale": width_scale,
            "height_scale": height_scale,
            "bind_ratio": self.bind_ratio_var.get()
        }

    def get_watermark_image(self):
        return self.original_watermark_image