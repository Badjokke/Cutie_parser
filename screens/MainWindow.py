from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from components.bounding_box_image_view import BoundingBoxImageView
from eda.EventEmitter import EventEmitter


class MainWindow(QMainWindow):
    def __init__(self, emitter: EventEmitter):
        super().__init__()
        self.setWindowTitle("Some fancy title")
        self.setMinimumSize(QSize(800, 600))
        self.layout = QHBoxLayout()

        # self.layout.addWidget(ListView(self))
        self.layout.addWidget(BoundingBoxImageView("130b.PNG", parent=self, event_emitter=emitter))
        self.main_widget = QWidget()

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
