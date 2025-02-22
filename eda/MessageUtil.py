from eda.model.BytesMessage import BytesMessage
from eda.model.StringMessage import StringMessage


class MessageUtil:
    @staticmethod
    def build_bytes_message(body: bytes, message_header: str) -> BytesMessage:
        return BytesMessage(message_header, body)

    @staticmethod
    def build_string_message(body: str, message_header: str) -> StringMessage:
        return StringMessage(message_header, body)
