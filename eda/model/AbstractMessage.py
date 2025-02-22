from abc import ABC, abstractmethod
from eda.exception.MustOverrideException import MustOverrideException
class AbstractMessage(ABC):
    def __init__(self, message_header: str, body):
        pass

    @abstractmethod
    def get_message_body(self):
        raise MustOverrideException("No default implementation provided!")
    @abstractmethod
    def get_message_header(self) -> str:
        raise MustOverrideException("No default implementation provided!")