import tkinter as tk
from tkinter import ttk, font
from colorsys import hsv_to_rgb, rgb_to_hsv

class TextWatermarkFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")

        # --- Layout ---
        self.columnconfigure(1, weight=1)

        # --- Widgets ---
        # Text Input
        ttk.Label(self, text="Text:").grid(row=0, column=0, sticky="w", pady=2)
        self.text_entry = ttk.Entry(self)
        self.text_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=2)

        # Font Family
        ttk.Label(self, text="Font:").grid(row=1, column=0, sticky="w", pady=2)
        self.font_family = ttk.Combobox(self, state="readonly")
        # 使用固定的字体列表，确保与watermark.py中的字体映射表一致
        self.font_family['values'] = [
            "SimSun",           # 宋体
            "Microsoft YaHei",  # 微软雅黑
            "SimHei",           # 黑体
            "KaiTi",            # 楷体
            "FangSong",         # 仿宋
            "NSimSun",          # 新宋体
            "Arial"             # Arial
        ]
        self.font_family.grid(row=1, column=1, columnspan=2, sticky="ew", pady=2)
        self.font_family.set("SimSun")  # 默认设置为宋体

        # Font Size, Bold, Italic
        style_frame = ttk.Frame(self)
        style_frame.grid(row=2, column=1, columnspan=2, sticky="ew")
        style_frame.columnconfigure(1, weight=1)

        ttk.Label(self, text="Style:").grid(row=2, column=0, sticky="w", pady=2)

        self.font_size = ttk.Spinbox(style_frame, from_=1, to=500, increment=1)
        self.font_size.grid(row=0, column=0, sticky="w")
        self.font_size.set(36)

        self.bold_var = tk.BooleanVar()
        self.bold_button = ttk.Checkbutton(style_frame, text="B", style="Toolbutton", variable=self.bold_var)
        self.bold_button.grid(row=0, column=2, padx=(10, 2))

        self.italic_var = tk.BooleanVar()
        self.italic_button = ttk.Checkbutton(style_frame, text="I", style="Toolbutton", variable=self.italic_var)
        self.italic_button.grid(row=0, column=3, padx=2)

        # Font Color
        ttk.Label(self, text="Color:").grid(row=3, column=0, sticky="w", pady=2)
        self.font_color_var = tk.StringVar(value="#000000")
        self.color_button = tk.Button(self, bg=self.font_color_var.get(), width=3, command=self.open_color_chooser)
        self.color_button.grid(row=3, column=1, sticky="w")

        # Shadow
        ttk.Label(self, text="Shadow:").grid(row=5, column=0, sticky="w", pady=2)
        shadow_frame = ttk.Frame(self)
        shadow_frame.grid(row=5, column=1, columnspan=2, sticky="ew", pady=2)

        self.shadow_var = tk.BooleanVar()
        shadow_button = ttk.Checkbutton(shadow_frame, variable=self.shadow_var)
        shadow_button.pack(side=tk.LEFT)

        self.shadow_size_var = tk.IntVar(value=2)
        shadow_size_spinbox = ttk.Spinbox(shadow_frame, from_=1, to=10, increment=1, textvariable=self.shadow_size_var, width=5)
        shadow_size_spinbox.pack(side=tk.LEFT, padx=10)

        # Stroke
        ttk.Label(self, text="Stroke:").grid(row=4, column=0, sticky="w", pady=2)
        stroke_frame = ttk.Frame(self)
        stroke_frame.grid(row=4, column=1, columnspan=2, sticky="ew", pady=2)

        self.stroke_var = tk.BooleanVar()
        stroke_button = ttk.Checkbutton(stroke_frame, variable=self.stroke_var)
        stroke_button.pack(side=tk.LEFT)

        self.stroke_size_var = tk.IntVar(value=1)
        stroke_size_spinbox = ttk.Spinbox(stroke_frame, from_=1, to=10, increment=1, textvariable=self.stroke_size_var, width=5)
        stroke_size_spinbox.pack(side=tk.LEFT, padx=10)

        self.stroke_color_var = tk.StringVar(value="#000000")
        self.stroke_color_button = tk.Button(stroke_frame, bg=self.stroke_color_var.get(), width=3, command=self.open_stroke_color_chooser)
        self.stroke_color_button.pack(side=tk.LEFT)

        

    def _center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def open_color_chooser(self):
        def on_confirm(color):
            self.font_color_var.set(color)
            self.color_button.config(bg=color)
        ColorSpectrumDialog(self, init_color=self.font_color_var.get(), on_confirm=on_confirm)

    def open_stroke_color_chooser(self):
        def on_confirm(color):
            self.stroke_color_var.set(color)
            self.stroke_color_button.config(bg=color)
        ColorSpectrumDialog(self, init_color=self.stroke_color_var.get(), on_confirm=on_confirm)

    def set_color(self, color, window):
        self.font_color_var.set(color)
        self.color_button.config(bg=color)
        window.destroy()

    def open_stroke_color_chooser(self):
        color_chooser = tk.Toplevel(self)
        color_chooser.title("Choose Stroke Color")
        color_chooser.transient(self)
        color_chooser.grab_set()

        colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF"]
        for i, color in enumerate(colors):
            row = i // 4
            col = i % 4
            btn = tk.Button(color_chooser, bg=color, width=3, command=lambda c=color: self.set_stroke_color(c, color_chooser))
            btn.grid(row=row, column=col, padx=2, pady=2)

        self._center_window(color_chooser)

    def set_stroke_color(self, color, window):
        self.stroke_color_var.set(color)
        self.stroke_color_button.config(bg=color)
        window.destroy()

    def get_settings(self):
        """Returns the current text watermark settings."""
        return {
            "text": self.text_entry.get(),
            "font_family": self.font_family.get(),
            "font_size": int(self.font_size.get()),
            "bold": self.bold_var.get(),
            "italic": self.italic_var.get(),
            "font_color": self.font_color_var.get(),
            "shadow": self.shadow_var.get(),
            "shadow_size": self.shadow_size_var.get(),
            "stroke": self.stroke_var.get(),
            "stroke_size": self.stroke_size_var.get(),
            "stroke_color": self.stroke_color_var.get(),
        }


class ColorSpectrumDialog(tk.Toplevel):
    def __init__(self, parent, init_color="#000000", on_confirm=None):
        super().__init__(parent)
        self.title("选择颜色")
        self.transient(parent)
        self.grab_set()
        self.on_confirm = on_confirm
        spectrum_width, spectrum_height = 240, 160
        self.canvas = tk.Canvas(self, width=spectrum_width, height=spectrum_height)
        self.canvas.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
        for x in range(spectrum_width):
            for y in range(spectrum_height):
                h = x / spectrum_width
                s = 1.0
                v = 1.0 - y / spectrum_height
                r, g, b = hsv_to_rgb(h, s, v)
                color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
                self.canvas.create_line(x, y, x+1, y, fill=color)
        self.rgb_vars = [tk.IntVar(value=int(init_color[i:i+2], 16)) for i in (1, 3, 5)]
        def rgb_to_hsv_pos(r, g, b):
            h, s, v = rgb_to_hsv(r/255, g/255, b/255)
            x = int(h * spectrum_width)
            y = int((1.0 - v) * spectrum_height)
            return x, y
        def hsv_pos_to_rgb(x, y):
            h = x / spectrum_width
            s = 1.0
            v = 1.0 - y / spectrum_height
            r, g, b = hsv_to_rgb(h, s, v)
            return int(r*255), int(g*255), int(b*255)
        def draw_crosshair(x, y):
            self.canvas.delete('crosshair')
            self.canvas.create_line(x-5, y, x+5, y, fill='white', width=2, tags='crosshair')
            self.canvas.create_line(x, y-5, x, y+5, fill='white', width=2, tags='crosshair')
        def update_rgb_labels():
            for i, var in enumerate(self.rgb_vars):
                var.set(max(0, min(255, var.get())))
            self.rgb_label.config(text=f"RGB: {self.rgb_vars[0].get()}, {self.rgb_vars[1].get()}, {self.rgb_vars[2].get()}")
        def set_color_from_rgb():
            r, g, b = [var.get() for var in self.rgb_vars]
            draw_crosshair(*rgb_to_hsv_pos(r, g, b))
            update_rgb_labels()
        def on_rgb_entry_change(*args):
            set_color_from_rgb()
        def on_canvas_click(event):
            x, y = event.x, event.y
            r, g, b = hsv_pos_to_rgb(x, y)
            for i, var in enumerate(self.rgb_vars):
                var.set([r, g, b][i])
            draw_crosshair(x, y)
            update_rgb_labels()
        self.canvas.bind('<Button-1>', on_canvas_click)
        self.rgb_label = tk.Label(self, text="RGB: 0, 0, 0")
        self.rgb_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        def rgb_entry_validate(P):
            try:
                v = int(P)
                return 0 <= v <= 255 or P == ""
            except:
                return False
        vcmd = (self.register(rgb_entry_validate), '%P')
        self.rgb_entries = []
        for i in range(3):
            entry = tk.Entry(self, width=4, textvariable=self.rgb_vars[i], validate='key', validatecommand=vcmd)
            entry.grid(row=1, column=i+1, padx=2, pady=5)
            entry.bind('<FocusOut>', lambda e, idx=i: self.rgb_vars[idx].set(max(0, min(255, self.rgb_vars[idx].get()))))
            entry.bind('<KeyRelease>', lambda e: on_rgb_entry_change())
            self.rgb_entries.append(entry)
        def confirm():
            color = f'#{self.rgb_vars[0].get():02x}{self.rgb_vars[1].get():02x}{self.rgb_vars[2].get():02x}'
            if self.on_confirm:
                self.on_confirm(color)
            self.destroy()
        def cancel():
            self.destroy()
        confirm_btn = tk.Button(self, text="确认", command=confirm)
        confirm_btn.grid(row=2, column=1, pady=10)
        cancel_btn = tk.Button(self, text="取消", command=cancel)
        cancel_btn.grid(row=2, column=2, pady=10)
        r, g, b = [var.get() for var in self.rgb_vars]
        x, y = rgb_to_hsv_pos(r, g, b)
        draw_crosshair(x, y)
        update_rgb_labels()
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
