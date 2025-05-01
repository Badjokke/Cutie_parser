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
import argparse
log = LoggerFactory.create_logger("MainApplication")

def parse_args():
    parser = argparse.ArgumentParser(description="Directory path")    
    parser.add_argument('--input_dir', type=str, default="dummy_data", required=False, help='Input path to directory with snippets')
    return parser.parse_args()

def load_items(args):
    assert args is not None and args.input_dir is not None, "input directory arg is mandatory"
    return Filesystem.load_directory_names(args.input_dir)

async def draw_main_screen(items: list[FileModel]):
    log.info("Creating event emitter")
    emitter = EventEmitter()
    log.info("Creating ocr")
    OcrWorker(OcrFactory.create_easyocr(), emitter)
    log.info("Starting main application")
    app = QApplication(sys.argv)
    window = MainWindow(emitter, items, "images/BUILDING")
    window.show()
    app.exec()
    log.info("Finished")


if __name__ == "__main__":
    asyncio.run(draw_main_screen(load_items(parse_args())))
