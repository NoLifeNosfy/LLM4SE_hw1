# This file will contain the UI for the watermark list section.
import tkinter as tk
from tkinter import ttk

class WatermarkListFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Watermarks", padding="10")
        ttk.Label(self, text="Watermark list will go here.").pack(side="left", fill="both", expand=True)
