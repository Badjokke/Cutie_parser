import asyncio
import sys

from PyQt6.QtWidgets import QApplication

from eda.EventEmitter import EventEmitter
from log.LoggerFactory import LoggerFactory
from ocr.OcrFactory import OcrFactory
from ocr.OcrWorker import OcrWorker
from screens.MainWindow import MainWindow

log = LoggerFactory.create_logger("MainApplication")


async def draw_main_screen():
    log.info("Creating event emitter")
    emitter = EventEmitter()
    log.info("Creating ocr")
    OcrWorker(OcrFactory.create_easyocr(), emitter)
    log.info("Starting main application")
    app = QApplication(sys.argv)
    window = MainWindow(emitter)
    window.show()
    app.exec()
    log.info("Finished")


if __name__ == "__main__":
    asyncio.run(draw_main_screen())
