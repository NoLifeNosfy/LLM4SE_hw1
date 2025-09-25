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
        scale_frame = ttk.Frame(self)
        scale_frame.pack(fill=tk.X, pady=5)

        ttk.Label(scale_frame, text="Scale (Width x Height):").pack(side=tk.LEFT, padx=5)
        self.scale_width_entry = ttk.Entry(scale_frame, width=5)
        self.scale_width_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(scale_frame, text="x").pack(side=tk.LEFT)
        self.scale_height_entry = ttk.Entry(scale_frame, width=5)
        self.scale_height_entry.pack(side=tk.LEFT, padx=5)

        # --- JPEG Quality --- #
        quality_frame = ttk.Frame(self)
        quality_frame.pack(fill=tk.X, pady=5)

        ttk.Label(quality_frame, text="JPEG Quality:").pack(side=tk.LEFT, padx=5)
        self.quality_scale = ttk.Scale(quality_frame, from_=1, to=100, orient=tk.HORIZONTAL)
        self.quality_scale.set(95)
        self.quality_scale.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def browse_output_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def get_settings(self):
        return {
            "output_dir": self.output_path.get(),
            "prefix": self.prefix_entry.get(),
            "suffix": self.suffix_entry.get(),
            "scale_width": self.scale_width_entry.get(),
            "scale_height": self.scale_height_entry.get(),
            "jpeg_quality": int(self.quality_scale.get())
        }