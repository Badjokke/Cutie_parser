from PyQt6 import QtCore
from PyQt6.QtCore import Qt

from model.FileModel import FileModel


class FileListModel(QtCore.QAbstractListModel):
    def __init__(self, parent, items=list[FileModel], **kwargs):
        super().__init__(parent)
        self.item = items

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            status, text = self.item[index.row()]()
            return text

    def rowCount(self, index):
        return len(self.item)
