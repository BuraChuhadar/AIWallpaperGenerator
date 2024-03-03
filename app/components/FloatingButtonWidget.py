from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QApplication, QSizePolicy, QMenu, QAction, QStyle
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSlot
from PyQt5.QtCore import QEvent  # Make sure to import QEvent

from app.utils.wallpaper_functions import set_wallpaper, set_lockscreen


class FloatingButtonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.dataLoading = False
        self.imageData = None
        self.originalPixmap = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to use the entire space
        self.layout.setSpacing(0)  # Remove spacing between widgets

        self.imageLabel = QLabel(self)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setAlignment(Qt.AlignCenter)  # Center the image within the label
        self.layout.addWidget(self.imageLabel)

        self.refreshButton = QPushButton('Refresh', self)
        self.refreshButton.setStyleSheet("background-color: rgba(255, 255, 255, 127);")  # Set opacity to 50%
        self.refreshIcon = self.style().standardIcon(QStyle.SP_BrowserReload)  # Get the standard refresh icon
        self.refreshButton.setIcon(self.refreshIcon)

        self.refreshButton.clicked.connect(self.onClick)
        self.refreshButton.hide()  # Initially hidden

        self.imageLabel.setMouseTracking(True)
        self.refreshButton.setMouseTracking(True)

        self.imageLabel.installEventFilter(self)
        self.refreshButton.installEventFilter(self)

    @pyqtSlot()
    def onClick(self):
        self.parent.onGenerateWallpaperButtonClicked()

    def isLoading(self):
        if self.dataLoading or not self.originalPixmap:
            self.refreshButton.hide()
            return True
        return False

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseMove:
            if not self.isLoading():
                self.positionAndShowRefreshButton()
                return True
        elif event.type() == QEvent.Enter:
            if not self.isLoading() and obj == self.imageLabel or obj == self.refreshButton:
                # Show the button when the mouse enters the image or button
                self.positionAndShowRefreshButton()
                return True
        elif event.type() == QEvent.Leave:
            if not self.isLoading() and obj == self.imageLabel:
                # Use a QTimer to delay the hide action, checking cursor position
                QTimer.singleShot(100, self.checkAndHideRefreshButton)
            elif obj == self.refreshButton:
                # Hide immediately if leaving the button and not entering the label immediately
                self.checkAndHideRefreshButton()
            return True
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        if self.originalPixmap:
            # Calculate a scaled pixmap that respects the window's size and the image's aspect ratio
            newSize = self.size()  # or some calculation based on self.minimumSize() and aspect ratio
            scaledPixmap = self.originalPixmap.scaled(newSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.imageLabel.setPixmap(scaledPixmap)
        super().resizeEvent(event)

    def positionAndShowRefreshButton(self):
        if not self.originalPixmap:
            return
        # Center the refreshButton over the imageLabel
        self.refreshButton.move(self.width() // 2 - self.refreshButton.width() // 2,
                                self.height() // 2 - self.refreshButton.height() // 2)
        self.refreshButton.show()

    def checkAndHideRefreshButton(self):
        # Hide the button if the cursor is not over the label or button
        if not (self.imageLabel.rect().contains(self.imageLabel.mapFromGlobal(QCursor.pos())) or
                self.refreshButton.rect().contains(self.refreshButton.mapFromGlobal(QCursor.pos()))):
            self.refreshButton.hide()

    def setImage(self, pixmap):
        self.originalPixmap = pixmap
        self.imageLabel.setPixmap(pixmap)

    def setImageData(self, imageData):
        self.imageData = imageData

    def setText(self, text):
        self.imageLabel.setText(text)

    def setIsLoading(self, isLoading):
        self.dataLoading = isLoading
        if isLoading:
            self.refreshButton.hide()
        else:
            self.positionAndShowRefreshButton()
