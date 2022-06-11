import time

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets
from qt_form import Ui_MainWindow
import requests
import json
from utils.Constant import *

VIETSTOCK_END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2"
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
COLUMN_NAME = ["Status", "Giá mua", "Giá HT", "Lãi/Lỗ", "% Max-HT", "Min week", "Time",
               "Max week", "Time", "% Max-Min",
               "% Cắt lỗ", "% Bán", "Trần", "Sàn", "Sound"]


class MainUI:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.data_vietstock = None
        self.data_from_file = None
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
            self.data_from_file = json.load(file_data)
            self.data_from_file = dict(
                sorted(self.data_from_file.items(), key=lambda item:item[1]["follow"], reverse=True))
            row_number = len(self.data_from_file)
            self.uic.tableWidget.setGeometry(QtCore.QRect(30, 10, 1050, 521))
            self.uic.tableWidget.setColumnCount(len(COLUMN_NAME))
            self.uic.tableWidget.setRowCount(row_number)
            _translate = QtCore.QCoreApplication.translate

            # column
            for column_index, column_name in enumerate(COLUMN_NAME):
                item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setHorizontalHeaderItem(column_index, item)
                item.setText(_translate("MainWindow", column_name))

            # row
            for row_index, stock_code in enumerate(self.data_from_file):
                item_dict = self.data_from_file[stock_code]
                item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setVerticalHeaderItem(row_index, item)
                item.setText(_translate("MainWindow", stock_code))

                # data body
                item = QtWidgets.QTableWidgetItem()
                try:
                    gia_da_mua = int(item_dict.get("bought"))
                except TypeError:
                    gia_da_mua = 0
                self.uic.tableWidget.setItem(row_index, CONSTANT_BOUGHT, item)
                item.setText(_translate("MainWindow", str(gia_da_mua)))
