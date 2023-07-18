from PySide6.QtWidgets import QMainWindow
from widget_ui import MainUI
class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.resize(600, 600)
        self.setWindowTitle("pyside6tut")

        widget = MainUI(self)

        self.setCentralWidget(widget)
        widget.show()


