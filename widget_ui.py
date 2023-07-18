from PySide6.QtCore import QRect
from PySide6.QtWidgets import QWidget, QMainWindow, QPushButton
from key_constructor import octave

class MainUI(QWidget):
    def __init__(self, window):
        super().__init__()
        self.setParent(window)
        window.resize(800, 200)
        
        self.keyboard = octave(window)

