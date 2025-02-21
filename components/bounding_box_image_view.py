from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QPainter


class BoundingBoxImageView(QWidget):
    def __init__(self, image:str, parent=None):
        super().__init__(parent)
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 300, 300
        self.painter: QPainter|None = None

        pixmap = QPixmap(image)
        self.label = QLabel(self)
        self.__init_canvas(pixmap)
        self.__draw_bounding_box(pixmap)

    def set_pix(self, img_path: str):
        self.painter.end()
        self.__init_canvas(QPixmap(img_path))

    def mouseMoveEvent(self, event):
        print("mouseMoveEvent")

    def mouseReleaseEvent(self, a0):
        print("release")



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
       self.__draw_rec(self.painter, (self.x1, self.x2, self.y1, self.y2))
       self.label.setPixmap(canvas)
