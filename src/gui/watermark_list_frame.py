import tkinter as tk
from tkinter import ttk, simpledialog

class WatermarkListFrame(ttk.LabelFrame):
    def __init__(self, parent, on_load_callback, on_save_callback, on_delete_callback):
        super().__init__(parent, text="Watermark Templates", padding="10")

        self.on_load_callback = on_load_callback
        self.on_save_callback = on_save_callback
        self.on_delete_callback = on_delete_callback

        # --- Layout ---
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # --- Template List ---
        list_frame = ttk.Frame(self)
        list_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=5)
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        self.template_listbox = tk.Listbox(list_frame, exportselection=False)
        self.template_listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.template_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.template_listbox.config(yscrollcommand=scrollbar.set)

        # --- Buttons ---
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(5,0))
        button_frame.columnconfigure((0, 1, 2), weight=1)

        load_button = ttk.Button(button_frame, text="Load", command=self._on_load_press)
        load_button.grid(row=0, column=0, padx=2)

        save_button = ttk.Button(button_frame, text="Save Current", command=self._on_save_press)
        save_button.grid(row=0, column=1, padx=2)

        delete_button = ttk.Button(button_frame, text="Delete", command=self._on_delete_press)
        delete_button.grid(row=0, column=2, padx=2)

    def _on_load_press(self):
        if self.on_load_callback:
            self.on_load_callback()

    def _on_save_press(self):
        if self.on_save_callback:
            template_name = simpledialog.askstring("Save Template", "Enter a name for the template:", parent=self)
            if template_name:
                self.on_save_callback(template_name)

    def _on_delete_press(self):
        if self.on_delete_callback:
            self.on_delete_callback()

    def get_selected_template(self):
        """Returns the name of the currently selected template."""
        selected_indices = self.template_listbox.curselection()
        if not selected_indices:
            return None
        return self.template_listbox.get(selected_indices[0])

    def update_template_list(self, templates):
        """Clears and repopulates the listbox with template names."""
        self.template_listbox.delete(0, tk.END)
        for name in sorted(templates):
            self.template_listbox.insert(tk.END, name)