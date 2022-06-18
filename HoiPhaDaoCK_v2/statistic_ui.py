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
        self.uic = Ui_Dialog()
        self.uic.setupUi(self.window)
        self.window.show()
        self.show_table()

    def show_table(self):
        nhom_nganh = []
        for nganh in NHOM_CO_PHIEU:
            if nganh == FILE_DA_MUA or nganh == FILE_VN30 or nganh == FILE_VN100  or nganh == FILE_TAT_CA:
                continue
            nhom_nganh.append(NHOM_CO_PHIEU[nganh]["name"])
        self.uic.tableWidget.setRowCount(len(nhom_nganh))
        self.uic.tableWidget.setColumnCount(5)
        _translate = QtCore.QCoreApplication.translate
        for row_index, ten_nganh in enumerate(nhom_nganh):
            item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setVerticalHeaderItem(row_index, item)
            item.setText(_translate("MainWindow", ten_nganh))


