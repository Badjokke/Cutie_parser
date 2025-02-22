from eda.model.AbstractMessage import AbstractMessage
class StringMessage(AbstractMessage):
    def __init__(self, message_header: str, body: str):
        super().__init__(message_header, body)
        self.__body = body
        self.__message_header = message_header

    def get_message_body(self) -> str:
        return self.__body

    def get_message_header(self) -> str:
        return self.__message_header
