import tkinter as tk
from colorsys import hsv_to_rgb, rgb_to_hsv

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