from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from logging import getLogger
from typing import Callable

from eda.model.AbstractMessage import AbstractMessage


class EventChannels(Enum):
    OCR_CHANNEL = "OCR_CHANNEL"
    OCR_TEXT_CHANNEL = "OCR_TEXT_CHANNEL"
    IMAGE_SELECTED_CHANNEL = "IMAGE_SELECTED_CHANNEL"


class EventEmitter:
    def __init__(self, pool_size: int = 5):
        self.__subscribers: dict[str, list[Callable[[AbstractMessage], None]]] = {}
        self.__threadpool = ThreadPoolExecutor(max_workers=pool_size)
        self.logger = getLogger(self.__class__.__name__)

    def add_consumer(self, channel: str, callback: Callable[[AbstractMessage], None]):
        self.logger.info(f"Adding consumer to {channel}")
        if channel not in self.__subscribers:
            self.__subscribers[channel] = []
        self.__subscribers[channel].append(callback)

    def emit_event(self, message: AbstractMessage):
        self.logger.info(f"Emitting to channel: {message.get_message_header()}\ncontent: {message.get_message_body()}")
        for callback in self.__subscribers[message.get_message_header()]:
            self.__threadpool.submit(callback, message)
