from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from components.listview import ListView
from components.bounding_box_image_view import BoundingBoxImageView
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Some fancy title")
        self.layout = QHBoxLayout()

        self.layout.addWidget(ListView(self))
        self.layout.addWidget(BoundingBoxImageView("130b.PNG",self))
        self.main_widget = QWidget()

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)