from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QSpacerItem, QSizePolicy, QLineEdit, QPushButton, \
    QTextEdit

from components.bounding_box_image_view import BoundingBoxImageView
from components.listview import ListView
from eda.EventEmitter import EventEmitter


class MainWindow(QMainWindow):
    def __init__(self, emitter: EventEmitter):
        super().__init__()
        self.emitter = emitter

        self.setWindowTitle("Some fancy title")
        self.setMinimumSize(QSize(1024, 680))

        self.layout = self.setup_layout(self.create_grid_layout())

        self.ocr_scan_input = self.create_input("ocr_dummy_input")
        self.label_input = self.create_input("label_input")

        self.submitButton = QPushButton("Submit")

        self.build_upper_screen_part()
        self.layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed), 1, 0, 1, 3)
        self.build_lower_screen_part()

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    @staticmethod
    def create_grid_layout(spacing: int = 10) -> QGridLayout:
        layout = QGridLayout()
        layout.setSpacing(spacing)
        return layout

    @staticmethod
    def setup_layout(layout: QGridLayout) -> QGridLayout:
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(2, 1)
        layout.setRowStretch(0, 3)
        layout.setRowStretch(2, 1)
        return layout

    def create_input(self, placeholder: str = None) -> QLineEdit:
        qt_input = QLineEdit(parent=self)
        if placeholder is not None:
            qt_input.setPlaceholderText(placeholder)
        return qt_input

    def build_upper_screen_part(self):
        self.layout.addWidget(BoundingBoxImageView("130b.PNG", parent=self, event_emitter=self.emitter), 0, 0)
        self.layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum), 0, 1)
        self.layout.addWidget(ListView(parent=self, event_emitter=self.emitter))

    def build_lower_screen_part(self):
        self.layout.addWidget(QTextEdit(parent=self), 2, 2)
        self.layout.addWidget(self.ocr_scan_input, 3, 0)
        self.layout.addWidget(self.label_input, 3, 1)
        self.layout.addWidget(self.submitButton, 3, 2)
