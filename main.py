import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from model.FileListModel import FileListModel
from model.FileModel import FileModel
from eda.EventEmitter import EventEmitter
from log.LoggerFactory import LoggerFactory
from ocr.OcrFactory import OcrFactory
from ocr.OcrWorker import OcrWorker
from screens.MainWindow import MainWindow
from filesystem.filesystem import Filesystem
log = LoggerFactory.create_logger("MainApplication")

def load_items():
    return Filesystem.load_directory_names("B:\dipl\dataset\CUSTOM_DATASET\MISC")

async def draw_main_screen(items: list[FileModel]):
    log.info("Creating event emitter")
    emitter = EventEmitter()
    log.info("Creating ocr")
    OcrWorker(OcrFactory.create_easyocr(), emitter)
    log.info("Starting main application")
    app = QApplication(sys.argv)
    window = MainWindow(emitter, items, "MICS")
    window.show()
    app.exec()
    log.info("Finished")


if __name__ == "__main__":
    asyncio.run(draw_main_screen(load_items()))
