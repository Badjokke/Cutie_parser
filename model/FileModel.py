from PyQt6 import QtCore
from PyQt6.QtCore import Qt


class FileModel(QtCore.QAbstractListModel):
    def __init__(self, *args, items=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.todos = items or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            text = self.todos[index.row()]
            return text

    def rowCount(self, index):
        return len(self.todos)
