from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMenu, QAction, QLabel, QVBoxLayout, QWidget


class ImageWidget(QWidget):
    def __init__(self, imageData, mainWindow, parent=None):
        super().__init__(parent)
        self.imageData = imageData
        self.mainWindow = mainWindow
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        image = QImage.fromData(self.imageData)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self.label)
        self.setLayout(layout)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        setWallpaper = QAction("Set as Wallpaper", self)
        setLockscreen = QAction("Set as Lockscreen", self)
        contextMenu.addAction(setWallpaper)
        contextMenu.addAction(setLockscreen)

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == setWallpaper:
            self.mainWindow.set_wallpaper(self.imageData)
        elif action == setLockscreen:
            self.mainWindow.set_lockscreen(self.imageData)  # Assuming this method exists
