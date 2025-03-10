from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy

from components.util.util import Util
from eda.EventEmitter import EventEmitter, EventChannels
from eda.MessageUtil import MessageUtil
from log.LoggerFactory import LoggerFactory


class BoundingBoxImageView(QWidget):
    def __init__(self, image: str, event_emitter: EventEmitter, parent=None):
        super().__init__(parent)
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.painter: QPainter | None = None
        self.box_start = False
        self.pixmap = QPixmap(image)
        self.label = QLabel(self)

        self.canvas = QPixmap(self.pixmap.size())
        self.canvas_label = QLabel(self)

        self.event_emitter = event_emitter
        self.logger = LoggerFactory.create_logger(self.__class__.__name__)
        self.__init_canvas()

    def mouseMoveEvent(self, event):
        x, y = self.__parse_event_position(event)
        self.set_box_start(x, y)

    def mouseReleaseEvent(self, event):
        self.box_start = False
        x, y = self.__parse_event_position(event)
        self.x2 = x
        self.y2 = y
        rect: QRect = self.__draw_bounding_box()
        captured = self.__capture_img(rect)
        captured.save("capture.png")
        self.emit_ocr_message(captured)

        # self.remove_bounding_box(rect)

    def set_box_start(self, x1, y1):
        if self.box_start is False:
            self.box_start = True
            self.x1 = x1
            self.y1 = y1

    def remove_bounding_box(self, rect: QRect):
        self.logger.info("Removing bounding box from scene")
        self.painter.eraseRect(rect)
        self.__reset_canvas()

    def __capture_img(self, capture_box: QRect) -> QPixmap:
        return self.label.pixmap().copy(capture_box)

    def emit_ocr_message(self, pixmap: QPixmap):
        self.logger.info("Emitting ocr message")
        self.event_emitter.emit_event(
            MessageUtil.build_bytes_message(Util.pixmap_to_bytes(pixmap), EventChannels.OCR_CHANNEL.value))

    @staticmethod
    def __draw_rec(painter, rect: QRect):
        painter.drawRect(rect)

    def __init_canvas(self):
        self.painter = QPainter(self.canvas)
        self.label.setPixmap(self.pixmap)
        self.label.setMinimumSize(self.pixmap.size())
        self.__reset_canvas()

    def __reset_canvas(self):
        self.canvas.fill(Qt.GlobalColor.transparent)
        self.label.setMinimumSize(self.pixmap.size())
        self.canvas_label.setPixmap(self.pixmap.copy())

    def __draw_bounding_box(self) -> QRect:
        rect = QRect(min(self.x1, self.x2), min(self.y1, self.y2), abs(self.x1 - self.x2), abs(self.y1 - self.y2))
        self.logger.info(f"Drawing bounding box {rect}")
        self.__draw_rec(self.painter, rect)
        # self.canvas_label.setPixmap(self.canvas)
        return rect

    @staticmethod
    def __parse_event_position(event) -> tuple[int, int]:
        return int(event.position().x()), int(event.position().y())

    def set_new_canvas(self, image_path):
        self.logger.info(f"Setting new canvas with image: {image_path}")
        self.pixmap = QPixmap(image_path)
        # self.setMinimumSize(self.pixmap.size())
        self.painter.end()
        self.__init_canvas()
