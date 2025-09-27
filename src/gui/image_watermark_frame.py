import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class ImageWatermarkFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        
        # 初始化变量
        self.watermark_image = None
        self.watermark_preview = None
        
        # 创建图片水印选择区域
        # 图片选择按钮
        select_image_frame = ttk.Frame(self)
        select_image_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(select_image_frame, text="选择水印图片:").pack(side=tk.LEFT, padx=(0, 10))
        self.image_path_var = tk.StringVar()
        ttk.Entry(select_image_frame, textvariable=self.image_path_var, width=30).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(select_image_frame, text="浏览...", command=self.browse_watermark_image).pack(side=tk.LEFT, padx=5)
        
        # 图片预览区域
        preview_frame = ttk.LabelFrame(self, text="水印预览", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.image_preview_label = ttk.Label(preview_frame)
        self.image_preview_label.pack(fill=tk.BOTH, expand=True)
    
    def browse_watermark_image(self):
        """打开文件对话框选择水印图片"""
        file_path = filedialog.askopenfilename(
            title="选择水印图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            self.image_path_var.set(file_path)
            try:
                # 加载水印图片
                self.watermark_image = Image.open(file_path)
                # 显示预览
                self.update_watermark_preview()
            except Exception as e:
                print(f"加载图片时出错: {e}")
    
    def update_watermark_preview(self):
        """更新水印图片预览"""
        if self.watermark_image:
            # 创建预览图像（缩放到合适大小）
            preview_width = 200
            preview_height = 200
            
            # 保持宽高比的缩放
            img_width, img_height = self.watermark_image.size
            ratio = min(preview_width / img_width, preview_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            preview_img = self.watermark_image.resize((new_width, new_height), Image.LANCZOS)
            
            # 转换为Tkinter可用的格式
            self.watermark_preview = ImageTk.PhotoImage(preview_img)
            self.image_preview_label.config(image=self.watermark_preview)
    
    def get_watermark_image(self):
        """返回当前选择的水印图片"""
        return self.watermark_image