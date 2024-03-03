import base64
import sqlite3
import sys
import tempfile

import requests
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMainWindow
from PyQt5.QtCore import Qt, pyqtSlot, QPoint
from PyQt5.QtGui import QPixmap

from app.components.FloatingButtonWidget import FloatingButtonWidget
from app.components.HoverLabel import HoverLabel
from app.views.historical_wallpapers import HistoricalWallpapersWindow
from app.init_db import initialize_db
from app.utils.wallpaper_functions import set_wallpaper
from app.wallpaper_api import OpenAIWallpaperGenerator

# Initialize the OpenAI Wallpaper Generator with your API key
api_key = ""  # Replace with your actual OpenAI API key
wallpaper_generator = OpenAIWallpaperGenerator(api_key)


class WallpaperGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        initialize_db()  # Initialize the database
        self.title = 'Wallpaper Generator'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 520  # Adjusted height to accommodate the resolution dropdown
        self.selected_resolution = '1024x768'  # Default resolution
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        self.label = QLabel('Enter Description:', self)
        self.label.setMaximumHeight(20)
        layout.addWidget(self.label)

        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        # Resolution dropdown
        self.resolutionDropdown = QComboBox(self)
        self.resolutionDropdown.addItem('800x600')  # 4:3
        self.resolutionDropdown.addItem('1024x768')  # 4:3
        self.resolutionDropdown.addItem('1280x720')  # 16:9, HD
        self.resolutionDropdown.addItem('1366x768')  # ~16:9, common laptop screen
        self.resolutionDropdown.addItem('1600x900')  # 16:9
        self.resolutionDropdown.addItem('1920x1080')  # 16:9, Full HD
        self.resolutionDropdown.addItem('1024x1024')  # Square
        self.resolutionDropdown.addItem('1024x1792')  # Portrait
        self.resolutionDropdown.addItem('1792x1024')  # Landscape
        self.resolutionDropdown.addItem('2560x1440')  # 16:9, QHD
        self.resolutionDropdown.addItem('3440x1440')  # 21:9, UltraWide
        self.resolutionDropdown.addItem('3840x2160')  # 16:9, 4K UHD
        layout.addWidget(self.resolutionDropdown)

        self.button = QPushButton('Generate Wallpaper', self)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        # Use FloatingButtonWidget for image display and refresh functionality
        self.floatingButtonWidget = FloatingButtonWidget(self)
        layout.addWidget(self.floatingButtonWidget)

        self.showGalleryButton = QPushButton('Show Wallpaper Gallery', self)
        self.showGalleryButton.clicked.connect(
            self.show_wallpaper_gallery)  # Assume show_wallpaper_gallery method exists
        layout.addWidget(self.showGalleryButton)

        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def show_wallpaper_gallery(self):
        self.galleryWindow = HistoricalWallpapersWindow()
        self.galleryWindow.show()
    def generate_wallpaper(self):
        description = self.textbox.text()
        self.selected_resolution = self.resolutionDropdown.currentText()
        # Assuming generate_wallpaper method returns an image at the highest available resolution
        image_url = wallpaper_generator.generate_wallpaper(description,
                                                           '1024x1024')  # Use the highest available resolution
        if image_url:
            self.download_and_display_image(image_url, self.selected_resolution)
            print("Wallpaper generated successfully.")
        else:
            self.floatingButtonWidget.setText("Failed to generate wallpaper.")
            print("Failed to generate wallpaper.")
    @pyqtSlot()
    def on_click(self):
        self.generate_wallpaper()


    def download_and_display_image(self, image_url, target_resolution):
        try:
            response = requests.get(image_url)
            response.raise_for_status()

            image_data = response.content
            # Write the binary data to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_image:
                temp_image.write(image_data)
                temp_image_path = temp_image.name
                print(f'temp image path {temp_image_path}')

            # Check if upscaling is needed
            width, height = map(int, target_resolution.split('x'))
            if width > 1024 or height > 1024:  # Assuming 1024x1024 is the max without upscaling
                self.upscale_image(temp_image_path, width, height)

            # Display Image in QLabel
            pixmap = QPixmap(temp_image_path)
            self.floatingButtonWidget.set_image(
                pixmap.scaled(self.floatingButtonWidget.width(), self.floatingButtonWidget.height(), Qt.KeepAspectRatio))

            # Insert wallpaper record into the database
            # Decode the Base64 string to binary data
            image_data = base64.b64encode(response.content).decode('utf-8')
            self.insert_wallpaper(self.textbox.text(), target_resolution, image_data)

            # Set the image as wallpaper
            set_wallpaper(response.content)
        except Exception as e:
            self.floatingButtonWidget.set_text("Failed to download or display wallpaper.")
            print(f"Error: {e}")

    def upscale_image(self, image_path, target_width, target_height):
        print(f'upscaling {image_path}')
        img = Image.open(rf"{image_path}")
        img_resized = img.resize((target_width, target_height), Image.LANCZOS)
        img_resized.save(image_path)
        print('image is upscaled')

    def insert_wallpaper(self, description, resolution, image_data, db_path='wallpaper_db.sqlite'):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Insert the new record with the Base64-encoded image data
        cursor.execute("INSERT INTO wallpapers (description, resolution, image_data) VALUES (?, ?, ?)",
                       (description, resolution, image_data))
        conn.commit()
        conn.close()


def main():
    app = QApplication(sys.argv)
    ex = WallpaperGeneratorApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
