from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QWidget, QLabel

from components.util.util import Util
from eda.EventEmitter import EventEmitter, EventChannels
from eda.MessageUtil import MessageUtil


class BoundingBoxImageView(QWidget):
    def __init__(self, image: str, event_emitter: EventEmitter, parent=None):
        super().__init__(parent)
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.painter: QPainter | None = None
        self.box_start = False
        self.pixmap = QPixmap(image)
        self.label = QLabel(self)
        self.event_emitter = event_emitter
        self.__init_canvas(self.pixmap)

    def set_pix(self, img_path: str):
        self.painter.end()
        self.__init_canvas(QPixmap(img_path))

    def mouseMoveEvent(self, event):
        x, y = self.__parse_event_position(event)
        self.set_box_start(x, y)

    def mouseReleaseEvent(self, event):
        self.box_start = False
        x, y = self.__parse_event_position(event)
        self.x2 = x
        self.y2 = y
        rect: QRect = self.__draw_bounding_box(self.pixmap)
        captured = self.__capture_img(rect)
        self.event_emitter.emit_event(
            MessageUtil.build_bytes_message(Util.pixmap_to_bytes(captured), EventChannels.OCR_CHANNEL.value))
        captured.save("capture.png")
        # self.painter.eraseRect(rect)

    def set_box_start(self, x1, y1):
        if self.box_start is False:
            self.box_start = True
            self.x1 = x1
            self.y1 = y1

    def __capture_img(self, capture_box: QRect) -> QPixmap:
        return self.label.pixmap().copy(capture_box)

    @staticmethod
    def __draw_rec(painter, rect: QRect):
        painter.drawRect(rect)

    def __init_canvas(self, pixmap: QPixmap):
        self.painter = QPainter(pixmap)
        self.label.setPixmap(pixmap)

    def __draw_bounding_box(self, canvas) -> QRect:
        rect = QRect(min(self.x1, self.x2), min(self.y1, self.y2), abs(self.x1 - self.x2), abs(self.y1 - self.y2))
        self.__draw_rec(self.painter, rect)
        self.label.setPixmap(canvas)
        return rect

    @staticmethod
    def __parse_event_position(event) -> tuple[int, int]:
        return int(event.position().x()), int(event.position().y())
