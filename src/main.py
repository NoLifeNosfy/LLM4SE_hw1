import sys
import os
import traceback

# Add the src directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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
