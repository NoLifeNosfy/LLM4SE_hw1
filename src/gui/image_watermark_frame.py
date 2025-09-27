import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class ImageWatermarkFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        
        # 初始化变量
        self.watermark_image = None
        self.watermark_preview = None
        self.original_watermark_image = None  # 存储原始水印图片（未缩放）
        
        # 创建图片水印选择区域
        # 图片选择按钮
        select_image_frame = ttk.Frame(self)
        select_image_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(select_image_frame, text="选择水印图片:").pack(side=tk.LEFT, padx=(0, 10))
        self.image_path_var = tk.StringVar()
        ttk.Entry(select_image_frame, textvariable=self.image_path_var, width=30).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(select_image_frame, text="浏览...", command=self.browse_watermark_image).pack(side=tk.LEFT, padx=5)
        
        # 添加缩放比例设置
        scale_frame = ttk.Frame(self)
        scale_frame.pack(fill=tk.X, pady=5)
        
        # 宽度缩放比例
        width_scale_frame = ttk.Frame(scale_frame)
        width_scale_frame.pack(fill=tk.X, pady=2)
        ttk.Label(width_scale_frame, text="宽度缩放比例:").pack(side=tk.LEFT, padx=(0, 10))
        self.width_scale_var = tk.StringVar(value="1.0")
        self.width_scale_entry = ttk.Entry(width_scale_frame, textvariable=self.width_scale_var, width=10)
        self.width_scale_entry.pack(side=tk.LEFT)
        
        # 高度缩放比例
        height_scale_frame = ttk.Frame(scale_frame)
        height_scale_frame.pack(fill=tk.X, pady=2)
        ttk.Label(height_scale_frame, text="高度缩放比例:").pack(side=tk.LEFT, padx=(0, 10))
        self.height_scale_var = tk.StringVar(value="1.0")
        self.height_scale_entry = ttk.Entry(height_scale_frame, textvariable=self.height_scale_var, width=10)
        self.height_scale_entry.pack(side=tk.LEFT)
        
        # 绑定长宽比选项
        bind_ratio_frame = ttk.Frame(scale_frame)
        bind_ratio_frame.pack(fill=tk.X, pady=2)
        self.bind_ratio_var = tk.BooleanVar(value=True)
        self.bind_ratio_check = ttk.Checkbutton(
            bind_ratio_frame, 
            text="绑定长宽比", 
            variable=self.bind_ratio_var
        )
        self.bind_ratio_check.pack(side=tk.LEFT)
        
        # 添加应用缩放按钮
        ttk.Button(scale_frame, text="应用缩放", command=self.apply_scale).pack(side=tk.RIGHT, padx=5)
        
        # 图片预览区域
        preview_frame = ttk.LabelFrame(self, text="水印预览(预览框大小为200*200，水印过大，预览框也只会显示缩放后的水印)", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=False, pady=10)
        
        self.image_preview_label = ttk.Label(preview_frame)
        self.image_preview_label.pack(fill=tk.BOTH, expand=True)
        
        # 绑定输入框变化事件
        self.width_scale_var.trace_add("write", self.on_width_scale_change)
        self.height_scale_var.trace_add("write", self.on_height_scale_change)
    
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
                self.original_watermark_image = Image.open(file_path).convert("RGBA")
                # 初始化水印图片（可能会被缩放）
                self.watermark_image = self.original_watermark_image.copy()
                
                # 计算预览框缩放比
                preview_width = 200
                preview_height = 200
                img_width, img_height = self.original_watermark_image.size
                
                # 如果图片大于预览框，计算缩放比
                if img_width > preview_width or img_height > preview_height:
                    scale_ratio = min(preview_width / img_width, preview_height / img_height)
                    # 四舍五入到一位小数
                    scale_ratio = round(scale_ratio, 1)
                    # 设置为编辑区长宽缩放比的默认值
                    self.width_scale_var.set(str(scale_ratio))
                    self.height_scale_var.set(str(scale_ratio))
                else:
                    # 图片小于预览框，使用默认值1.0
                    self.width_scale_var.set("1.0")
                    self.height_scale_var.set("1.0")
                
                # 应用缩放（确保预览显示正确的尺寸）
                self.apply_scale()
            except Exception as e:
                print(f"加载图片时出错: {e}")
    
    def on_width_scale_change(self, *args):
        """当宽度缩放比例改变时调用"""
        if self.bind_ratio_var.get() and self.watermark_image:
            try:
                # 如果绑定了长宽比，则同步更新高度缩放比例
                width_scale = float(self.width_scale_var.get())
                self.height_scale_var.set(f"{width_scale:.1f}")
            except ValueError:
                # 输入不是有效的浮点数
                pass
    
    def on_height_scale_change(self, *args):
        """当高度缩放比例改变时调用"""
        if self.bind_ratio_var.get() and self.watermark_image:
            try:
                # 如果绑定了长宽比，则同步更新宽度缩放比例
                height_scale = float(self.height_scale_var.get())
                self.width_scale_var.set(f"{height_scale:.1f}")
            except ValueError:
                # 输入不是有效的浮点数
                pass
    
    def apply_scale(self):
        """应用缩放比例到水印图片"""
        if not self.original_watermark_image:
            return
            
        try:
            width_scale = float(self.width_scale_var.get())
            height_scale = float(self.height_scale_var.get())
            
            # 确保缩放比例为正数
            if width_scale <= 0 or height_scale <= 0:
                print("缩放比例必须为正数")
                return
                
            # 获取原始尺寸
            orig_width, orig_height = self.original_watermark_image.size
            
            # 计算新尺寸
            new_width = int(orig_width * width_scale)
            new_height = int(orig_height * height_scale)
            
            # 应用缩放 - 使用原始图像进行缩放
            resized_image = self.original_watermark_image.resize(
                (new_width, new_height), 
                Image.LANCZOS
            )
            
            # 确保保留RGBA格式
            self.watermark_image = resized_image.convert("RGBA")
            
            # 打印调试信息
            print(f"原始尺寸: {orig_width}x{orig_height}")
            print(f"缩放比例: 宽={width_scale}, 高={height_scale}")
            print(f"新尺寸: {new_width}x{new_height}")
            print(f"实际尺寸: {self.watermark_image.size}")
            
            # 更新预览
            self.update_watermark_preview()
            
        except ValueError as e:
            print(f"应用缩放时出错: {e}")
    
    def update_watermark_preview(self):
        """更新水印图片预览"""
        if self.watermark_image:
            # 创建预览图像（缩放到合适大小）
            preview_width = 200
            preview_height = 200
            
            # 获取图片尺寸
            img_width, img_height = self.watermark_image.size
            
            # 判断图片是否需要缩放
            if img_width <= preview_width and img_height <= preview_height:
                # 图片小于预览框，不需要缩放
                preview_img = self.watermark_image.copy()
            else:
                # 图片大于预览框，需要按比例缩小
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