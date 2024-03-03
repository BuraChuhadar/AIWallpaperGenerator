import base64

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QGridLayout, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from app.utils.sqlite import get_wallpapers
from app.utils.wallpaper_functions import set_wallpaper
from app.components.ImageWidget import ImageWidget


class HistoricalWallpapersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wallpaper Gallery')
        self.setGeometry(100, 100, 600, 400)  # Adjust size as needed
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Use a QVBoxLayout for the central widget
        layout = QVBoxLayout(self.centralWidget)

        # Create a scroll area to contain the grid of images
        self.scrollArea = QScrollArea(self)
        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)  # Make the scroll area resizable

        # Create a grid layout for the images
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        layout.addWidget(self.scrollArea)

        self.populate_wallpapers_list()

    def populate_wallpapers_list(self):
        wallpapers = get_wallpapers()
        for row, wallpaper in enumerate(wallpapers):
            imageData = wallpaper[3]  # Assuming wallpaper[3] is the file path
            image = base64.b64decode(imageData)
            # Pass 'self' as the mainWindow reference
            imageWidget = ImageWidget(image, self, self.scrollAreaWidgetContents)
            self.gridLayout.addWidget(imageWidget, row // 4, row % 4)  # Adjust grid dimensions as needed

    def on_wallpaper_click(self, item):
        wallpapers = get_wallpapers()
        for wallpaper in wallpapers:
            if item.text() == f"{wallpaper[1]} - {wallpaper[2]}":
                self.set_wallpaper(wallpaper[3])  # Assuming this method sets the wallpaper
                break

    def set_wallpaper(self, imageData):
        # Set the image as wallpaper
        set_wallpaper(imageData)
    def set_lockscreen(self, imageData):
        # This method should implement setting the lockscreen based on the OS
        # For demonstration, let's assume it's similar to setting a wallpaper
        print("Lockscreen setting functionality needs to be implemented")
