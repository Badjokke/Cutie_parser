from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class Dialog(QDialog):
    def __init__(self, message: str, window_title: str = "Dialog", parent=None):
        super().__init__()

        self.setWindowTitle(window_title)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)

        layout = QVBoxLayout()
        message = QLabel(message)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.buttonBox.clicked.connect(self.accept)