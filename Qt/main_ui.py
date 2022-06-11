from PyQt5.QtWidgets import QMainWindow
from qt_form import Ui_MainWindow


class MainUI:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)

    def show(self):
        self.main_win.show()