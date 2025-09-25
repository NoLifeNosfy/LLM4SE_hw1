import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Watermark Tool")
        self.geometry("600x400")

        # Placeholder for GUI elements
        label = ttk.Label(self, text="Watermark configuration will go here.")
        label.pack(pady=20)

        # Button to start watermarking
        start_button = ttk.Button(self, text="Apply Watermark")
        start_button.pack(pady=10)
