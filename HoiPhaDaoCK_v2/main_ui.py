import time

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets
from qt_form import Ui_MainWindow
import requests
import json
from utils.Constant import *


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

    def get_item_dict(self, dict: dict, key: str):
        try:
            value = dict.get(key)
            if value == 0:
                return ""
            return str(value)
        except:
            return ""

    def draw_table(self):
        with open("data/stock_code.json") as file_data:
            self.data_from_file = json.load(file_data)
            self.data_from_file = dict(
                sorted(self.data_from_file.items(), key=lambda item: item[1]["follow"], reverse=True))
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
                stock_dict = self.data_from_file[stock_code]
                item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setVerticalHeaderItem(row_index, item)
                item.setText(_translate("MainWindow", stock_code))

                # data body
                # Giá đã mua
                item_bought = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, CONSTANT_BOUGHT, item_bought)
                item_bought.setText(_translate("MainWindow", self.get_item_dict(stock_dict, "bought")))

                # phần trăm cắt lỗ
                item_cut_loss = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, CONSTANT_PERCENT_CAT_LO, item_cut_loss)
                item_cut_loss.setText(_translate("MainWindow", self.get_item_dict(stock_dict, "percent_cut_loss")))
