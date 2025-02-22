import sys
from screens.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from ocr.OcrWorker import OcrWorker
from ocr.OcrFactory import OcrFactory
from eda.EventEmitter import EventEmitter
if __name__ == "__main__":
    emitter = EventEmitter()
    ocr_worker = OcrWorker(OcrFactory.create_easyocr(), emitter)
    app = QApplication(sys.argv)
    window = MainWindow(emitter)
    window.show()
    app.exec()
"""
from ocr.ocr_factory import create_easyocr
reader = create_easyocr()
text = reader.readtext("capture.png")
print(text)
"""