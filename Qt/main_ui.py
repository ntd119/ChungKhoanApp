import time

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets
from qt_form import Ui_MainWindow
import requests
import json

VIETSTOCK_END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2"
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }

class MainUI:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.data_vietstock = None
        self.run()

    def run(self):
        self.call_api_vietstock()
        self.draw_table()

    def show(self):
        self.main_win.show()

    def call_api_vietstock(self):
        vietstock_prams = {
            "sectorID": 0,
            "catID": 0,
            "capitalID": 0,
            "languageID": 1
        }
        try:
            response = requests.get(VIETSTOCK_END_POINT, params=vietstock_prams, headers=HEADERS)
            self.data_vietstock = response.json()
        except:
            print("Call vietstock error")
            time.sleep(5)
            self.call_api_vietstock()

    def draw_table(self):
        with open("data/stock_code.json") as file_data:
            stock_list = json.load(file_data)
            row_number = len(stock_list)
            self.uic.tableWidget.setGeometry(QtCore.QRect(30, 10, 1050, 321))
            self.uic.tableWidget.setColumnCount(20)
            self.uic.tableWidget.setRowCount(row_number)
            _translate = QtCore.QCoreApplication.translate
            # column
            item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setHorizontalHeaderItem(0, item)
            item.setText(_translate("MainWindow", "name"))

            # row
            row_index = -1
            for stock_item in stock_list:
                row_index +=1
                item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setVerticalHeaderItem(row_index, item)
                item.setText(_translate("MainWindow", stock_item))

