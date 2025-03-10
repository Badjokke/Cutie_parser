from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QListView, QWidget, QVBoxLayout

from eda.EventEmitter import EventEmitter, EventChannels
from eda.model.StringMessage import StringMessage
from log.LoggerFactory import LoggerFactory
from model.FileListModel import FileListModel
from model.FileModel import FileModel


class ListView(QWidget):
    def __init__(self, parent=None, items: list[FileModel] = [], event_emitter: EventEmitter = None):
        super().__init__(parent)
        self.event_emitter: EventEmitter = event_emitter
        self.listview = QListView()
        self.listview.setModel(FileListModel(parent, items))
        layout = QVBoxLayout()
        layout.addWidget(self.listview)
        self.setLayout(layout)
        self.items = items
        self.listview.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self.__connect_item_events()
        self.current_item_index = -1
        self.log = LoggerFactory.create_logger(self.__class__.__name__)

    def __connect_item_events(self):
        self.listview.clicked.connect(self.on_double_click)

    def on_double_click(self, index: QModelIndex):
        self.current_item_index = index.row()
        item = self.items[index.row()]
        self.__emit_new_item_selected_event(item)

    def __emit_new_item_selected_event(self, item: FileModel):
        self.log.info(f"Emitting select item event for item: {item.item_label}")
        self.event_emitter.emit_event(StringMessage(EventChannels.IMAGE_SELECTED_CHANNEL.value, item.get_item_value()))
