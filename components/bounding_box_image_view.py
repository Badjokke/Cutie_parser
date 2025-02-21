from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QPainter


class BoundingBoxImageView(QWidget):
    def __init__(self, image:str, parent=None):
        super().__init__(parent)
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 300, 300
        self.painter: QPainter|None = None
        self.box_start = False
        self.pixmap = QPixmap(image)
        self.label = QLabel(self)
        self.__init_canvas(self.pixmap)
        #self.__draw_bounding_box(self.pixmap)

    def set_pix(self, img_path: str):
        self.painter.end()
        self.__init_canvas(QPixmap(img_path))

    def mouseMoveEvent(self, event):
        x,y = self.__parse_event_position(event)
        self.set_box_start(x,y)
        print("mouseMoveEvent")

    def mouseReleaseEvent(self, event):
        self.box_start = False
        x,y = self.__parse_event_position(event)
        self.x2 = x
        self.y2 = y
        self.__draw_bounding_box(self.pixmap)

    def set_box_start(self, x1, y1):
        if self.box_start is False:
            self.box_start = True
            self.x1 = x1
            self.y1 = y1

    @staticmethod
    def __draw_rec(painter, coords: tuple[int, int, int, int]):
        painter.drawRect(coords[0], coords[1], coords[2], coords[3])

    def __init_draw(self):
        pass

    def __end_draw(self):
        pass

    def __init_canvas(self, pixmap: QPixmap):
        self.painter = QPainter(pixmap)
        self.label.setPixmap(pixmap)


    def __draw_bounding_box(self, canvas):
       self.__draw_rec(self.painter, (min(self.x1,self.x2), min(self.y1,self.y2), abs(self.x1-self.x2), abs(self.y1-self.y2)))
       self.label.setPixmap(canvas)


    @staticmethod
    def __parse_event_position(event) -> tuple[int, int]:
        return int(event.position().x()), int(event.position().y())