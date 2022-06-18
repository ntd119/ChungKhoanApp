import time

from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui
from qt_form import Ui_MainWindow
from statistic_form import Ui_Dialog
import requests
import json
from datetime import datetime
from utils.Constant import *
import unidecode


class StatisticUI:
    def __init__(self):
        self.window = QMainWindow()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

