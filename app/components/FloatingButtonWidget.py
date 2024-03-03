from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QApplication, QSizePolicy
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSlot
from PyQt5.QtCore import QEvent  # Make sure to import QEvent

class FloatingButtonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent=parent
        self.originalPixmap = None  # Store the original pixmap
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to use the entire space
        self.layout.setSpacing(0)  # Remove spacing between widgets

        self.imageLabel = QLabel(self)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setAlignment(Qt.AlignCenter)  # Center the image within the label
        self.layout.addWidget(self.imageLabel)

        self.refreshButton = QPushButton('Refresh', self)
        self.refreshButton.clicked.connect(self.on_click)
        self.refreshButton.hide()  # Initially hidden

        self.imageLabel.installEventFilter(self)
        self.refreshButton.installEventFilter(self)

    @pyqtSlot()
    def on_click(self):
        self.parent.generate_wallpaper()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            if obj == self.imageLabel or obj == self.refreshButton:
                # Show the button when the mouse enters the image or button
                self.positionAndShowRefreshButton()
                return True
        elif event.type() == QEvent.Leave:
            if obj == self.imageLabel:
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
    def set_image(self, pixmap):
        self.originalPixmap = pixmap
        self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def set_text(self, text):
        self.imageLabel.setText(text)
