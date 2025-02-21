import sys
from screens.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow

app = QApplication(sys.argv)

window = MainWindow()


window.show()


app.exec()