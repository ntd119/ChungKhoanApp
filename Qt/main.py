import sys

from PyQt5 import QtWidgets, uic
from qt_form import Ui_MainWindow

class Stock (QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Stock, self).__init__()
        self.setupUi(self)

app = QtWidgets.QApplication(sys.argv)

form = Stock()
form.show()
app.exec()