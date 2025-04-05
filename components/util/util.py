import json

from PyQt6.QtCore import QByteArray, QBuffer, QIODeviceBase
from PyQt6.QtGui import QPixmap


class Util:
    @staticmethod
    def pixmap_to_bytes(captured: QPixmap, format="png") -> bytes:
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODeviceBase.OpenModeFlag.WriteOnly)
        captured.save(buffer, format=format)
        byte_data = buffer.data().data()
        buffer.close()
        return byte_data

    @staticmethod
    def t17_jsonl_line(text: list[str], image: str, label: str):
        return json.dumps({"text": text, "image": [image], "label": label.split(" ")})
