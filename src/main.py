import sys
import os
import traceback

from gui.main_window import MainWindow

def main():
    """Initializes and runs the GUI application."""
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
