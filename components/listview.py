from model.FileModel import FileModel
from PyQt6.QtWidgets import QListView, QWidget
class ListView(QWidget):
    def __init__(self, parent=None):
        self.mock_data = FileModel(items=["file1", "file2", "file3"])
        super().__init__(parent)
        self.listview = QListView()
        self.listview.setModel(self.mock_data)