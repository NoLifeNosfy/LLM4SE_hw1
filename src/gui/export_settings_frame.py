import tkinter as tk
from tkinter import ttk, filedialog

class ExportSettingsFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Export Settings", padding="10")

        # --- Output Path --- #
        self.output_path = tk.StringVar()
        output_frame = ttk.Frame(self)
        output_frame.pack(fill=tk.X, pady=5)

        ttk.Label(output_frame, text="Output Folder:").pack(side=tk.LEFT, padx=5)
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path)
        output_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        browse_button = ttk.Button(output_frame, text="Browse...", command=self.browse_output_path)
        browse_button.pack(side=tk.LEFT, padx=5)

        # --- Prefix/Suffix --- #
        name_frame = ttk.Frame(self)
        name_frame.pack(fill=tk.X, pady=5)

        ttk.Label(name_frame, text="Filename Prefix:").pack(side=tk.LEFT, padx=5)
        self.prefix_entry = ttk.Entry(name_frame)
        self.prefix_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        ttk.Label(name_frame, text="Filename Suffix:").pack(side=tk.LEFT, padx=5)
        self.suffix_entry = ttk.Entry(name_frame)
        self.suffix_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # --- Scaling --- #
        scale_frame = ttk.LabelFrame(self, text="Image Scaling", padding=5)
        scale_frame.pack(fill=tk.X, pady=5)

        self.width_scale_var = tk.StringVar(value="1.0")
        self.height_scale_var = tk.StringVar(value="1.0")
        self.bind_ratio_var = tk.BooleanVar(value=True)

        width_frame = ttk.Frame(scale_frame)
        width_frame.pack(fill=tk.X, pady=2)
        ttk.Label(width_frame, text="Width Scale Ratio:", width=18).pack(side=tk.LEFT, padx=5)
        ttk.Entry(width_frame, textvariable=self.width_scale_var, width=10).pack(side=tk.LEFT)

        height_frame = ttk.Frame(scale_frame)
        height_frame.pack(fill=tk.X, pady=2)
        ttk.Label(height_frame, text="Height Scale Ratio:", width=18).pack(side=tk.LEFT, padx=5)
        ttk.Entry(height_frame, textvariable=self.height_scale_var, width=10).pack(side=tk.LEFT)

        bind_frame = ttk.Frame(scale_frame)
        bind_frame.pack(fill=tk.X, pady=2)
        ttk.Checkbutton(bind_frame, text="Bind Aspect Ratio", variable=self.bind_ratio_var).pack(side=tk.LEFT, padx=5)

        self.width_scale_var.trace_add("write", self._on_width_scale_change)
        self.height_scale_var.trace_add("write", self._on_height_scale_change)

        # --- JPEG Quality --- #
        quality_frame = ttk.Frame(self)
        quality_frame.pack(fill=tk.X, pady=5)

        ttk.Label(quality_frame, text="JPEG Quality:").pack(side=tk.LEFT, padx=5)
        self.quality_scale = ttk.Scale(quality_frame, from_=1, to=100, orient=tk.HORIZONTAL)
        self.quality_scale.set(95)
        self.quality_scale.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def _on_width_scale_change(self, *args):
        if self.bind_ratio_var.get():
            try:
                self.height_scale_var.set(self.width_scale_var.get())
            except (ValueError, tk.TclError):
                pass

    def _on_height_scale_change(self, *args):
        if self.bind_ratio_var.get():
            try:
                self.width_scale_var.set(self.height_scale_var.get())
            except (ValueError, tk.TclError):
                pass

    def browse_output_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def get_settings(self):
        try:
            width_ratio = float(self.width_scale_var.get())
        except ValueError:
            width_ratio = 1.0
        try:
            height_ratio = float(self.height_scale_var.get())
        except ValueError:
            height_ratio = 1.0

        return {
            "output_dir": self.output_path.get(),
            "prefix": self.prefix_entry.get(),
            "suffix": self.suffix_entry.get(),
            "width_scale_ratio": width_ratio,
            "height_scale_ratio": height_ratio,
            "jpeg_quality": int(self.quality_scale.get())
        }
