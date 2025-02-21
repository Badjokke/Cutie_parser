from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap


class ImageView(QWidget):
    def __init__(self, initial_image:str,  parent=None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.pixmap = QPixmap(initial_image)
        self.label.setPixmap(self.pixmap)


    def set_image(self, path: str):
        self.pixmap = QPixmap(path)
        self.label.setPixmap(self.pixmap)
