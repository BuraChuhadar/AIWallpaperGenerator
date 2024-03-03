import sys
from PyQt5.QtWidgets import QApplication
from app.views.gui import WallpaperGeneratorApp  # Adjust the import path based on your project structure


def main():
    # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Initialize the main window using your defined GUI class
    mainWindow = WallpaperGeneratorApp()
    mainWindow.show()  # Show the main window

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
