import sys

from PyQt5 import QtWidgets, uic

class Stock (QtWidgets.QMainWindow):
    def __init__(self):
        super(Stock, self).__init__()
        uic.loadUi("qt_form.ui", self)

app = QtWidgets.QApplication(sys.argv)

form = Stock()
form.show()
app.exec()