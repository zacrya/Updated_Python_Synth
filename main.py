import sys
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    window.resize(678, 415)

    sys.exit(app.exec())
