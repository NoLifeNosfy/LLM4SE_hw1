import sys
import os

# Add the src directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from gui.main_window import MainWindow

def main():
    """Initializes and runs the GUI application."""
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
