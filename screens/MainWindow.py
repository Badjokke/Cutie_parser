from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QSpacerItem, QSizePolicy, QLineEdit, QPushButton, \
    QTextEdit, QLabel

from components.bounding_box_image_view import BoundingBoxImageView
from components.dialog import Dialog
from components.listview import ListView
from components.util.util import Util
from eda.EventEmitter import EventEmitter, EventChannels
from eda.model.StringMessage import StringMessage
from log.LoggerFactory import LoggerFactory
from model.FileModel import FileModel


class MainWindow(QMainWindow):
    def __init__(self, emitter: EventEmitter, items: list[FileModel], image_prefix: str):
        super().__init__()
        self.emitter = emitter

        self.setWindowTitle("Some fancy title")
        self.setMinimumSize(QSize(1500, 1000))
        self.logger = LoggerFactory.create_logger(self.__class__.__name__)
        self.layout = self.setup_layout(self.create_grid_layout())
        self.listview = ListView(self, items, event_emitter=self.emitter)
        self.text_area = QTextEdit(parent=self)
        self.ocr_word_count = QLabel(text="0")
        self.ocr_scan_input = self.create_input("ocr_dummy_input")
        self.image_prefix = image_prefix
        self.label_word_count = QLabel(text="0")
        self.bounding_box = BoundingBoxImageView("130b.PNG", parent=self, event_emitter=self.emitter)

        self.label_input = self.create_input("label_input")
        self.label_input.textEdited.connect(self.set_label_count_label)
        self.submitButton = QPushButton("Submit")
        self.submitButton.setFixedSize(80, 60)

        self.build_upper_screen_part()
        self.layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed), 1, 0, 1, 3)
        self.build_lower_screen_part()

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.listen_to_ocr_channel()
        self.listen_to_image_change_channel()
        self.add_submit_button_action()

    def listen_to_ocr_channel(self):
        self.logger.info(f"Listen to {EventChannels.OCR_TEXT_CHANNEL.value}")
        self.emitter.add_consumer(EventChannels.OCR_TEXT_CHANNEL.value, lambda text: self.set_ocr_scan_input_text(text))

    def set_ocr_scan_input_text(self, text: StringMessage):
        self.logger.info(f"Setting ocr input text to {text}")
        self.ocr_scan_input.setText(text.get_message_body())
        self.ocr_word_count.setText(f"{len(text.get_message_body().split(' '))}")

    @staticmethod
    def create_grid_layout(spacing: int = 10) -> QGridLayout:
        layout = QGridLayout()
        layout.setSpacing(spacing)
        return layout

    @staticmethod
    def setup_layout(layout: QGridLayout) -> QGridLayout:
        layout.setColumnStretch(0, 3)
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
        self.layout.addWidget(self.bounding_box, 0, 0)
        self.layout.addWidget(self.listview, 0, 2)
        self.layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum), 0, 1)

    def build_lower_screen_part(self):
        self.layout.addWidget(self.text_area, 2, 2)

        self.layout.addWidget(self.ocr_word_count, 2, 0)
        self.layout.addWidget(self.ocr_scan_input, 3, 0)

        self.layout.addWidget(self.label_word_count, 2, 1)
        self.layout.addWidget(self.label_input, 3, 1)

        self.layout.addWidget(self.submitButton, 3, 2)

    def add_submit_button_action(self):
        self.logger.info("Submit button clicked")
        self.submitButton.clicked.connect(self.verify_and_append)

    def verify_and_append(self):
        word_count = int(self.ocr_word_count.text())
        label_count = int(self.label_word_count.text())
        self.logger.debug(f"Verifying word and label count. Word count {word_count}, label count {label_count}")
        image_relative = f"{self.image_prefix}/{self.listview.get_currently_selected_item_label()}"
        if word_count != label_count:
            self.logger.debug("Word and label count mismatch")
            #return self.show_dialog(f"Word count is not equal to label count. Words {word_count}, labels {label_count}")

        self.append_to_textarea(image_relative)

    def append_to_textarea(self, image_relative: str):
        self.logger.debug("Appending to text area")
        self.text_area.append(
            Util.t17_jsonl_line(self.filter_and_tokenize(self.ocr_scan_input.text()), image_relative,
                                self.label_input.text()))

    def show_dialog(self, message: str):
        Dialog(message, "Whoah there cowboy", parent=self).exec()

    def set_label_count_label(self):
        self.label_word_count.setText(f'{len(self.label_input.text().split(" "))}')

    def listen_to_image_change_channel(self):
        self.emitter.add_consumer(EventChannels.IMAGE_SELECTED_CHANNEL.value, self.set_new_item)

    def set_new_item(self, message: StringMessage):
        self.logger.info("Image selected event consumed")
        body = message.get_message_body()
        self.bounding_box.set_new_canvas(body)

    @staticmethod
    def filter_and_tokenize(text: str) -> list[str]:
        return list(filter(lambda token: len(token.strip()) > 0, text.split(" ")))