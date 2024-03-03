from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal


class HoverLabel(QLabel):
    mouseHover = pyqtSignal(bool)  # True if mouse enters, False if leaves

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)  # Enable mouse tracking

    def enterEvent(self, event):
        self.mouseHover.emit(True)  # Emit signal on mouse enter
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.mouseHover.emit(False)  # Emit signal on mouse leave
        super().leaveEvent(event)
