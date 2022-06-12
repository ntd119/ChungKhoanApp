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
        self.draw_table()
        self.update_table()

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

    def format_value(self, value):
        return "{:,.0f}".format(value)

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
            for column_index, dict_name in enumerate(COLUMN_NAME):
                item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setHorizontalHeaderItem(column_index, item)
                item.setText(_translate("MainWindow", COLUMN_NAME[dict_name]["name"]))

            # row
            for row_index, stock_code in enumerate(self.data_from_file):
                stock_dict = self.data_from_file[stock_code]
                item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setVerticalHeaderItem(row_index, item)
                item.setText(_translate("MainWindow", stock_code))

                # data body
                # Giá đã mua bought
                item_bought = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["bought"]["index"], item_bought)
                item_bought.setText(_translate("MainWindow", self.get_item_dict(stock_dict, "bought")))

                # phần trăm cắt lỗ percent_cut_loss
                item_cut_loss = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["percent_cut_loss"]["index"], item_cut_loss)
                item_cut_loss.setText(_translate("MainWindow", self.get_item_dict(stock_dict, "percent_cut_loss")))

                # phần trăm bán percent_sell
                item_sell = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["percent_sell"]["index"], item_sell)
                item_sell.setText(_translate("MainWindow", self.get_item_dict(stock_dict, "percent_sell")))

    def update_table(self):
        self.call_api_vietstock()
        _translate = QtCore.QCoreApplication.translate
        for row_index, stock_code in enumerate(self.data_from_file):
            item_dict = self.data_from_file[stock_code]
            stock_single = [row for row in self.data_vietstock if row["_sc_"] == stock_code.upper()]
            if len(stock_single) == 1:
               stock_single = stock_single[0]
               # giá trần _clp_
               gia_tran_item = QtWidgets.QTableWidgetItem()
               self.uic.tableWidget.setItem(row_index, COLUMN_NAME["tran_value"]["index"], gia_tran_item)
               gia_tran_item.setText(_translate("MainWindow", self.format_value(stock_single['_clp_'])))

               # giá sàn _fp_
               gia_san_item = QtWidgets.QTableWidgetItem()
               self.uic.tableWidget.setItem(row_index, COLUMN_NAME["san_value"]["index"], gia_san_item)
               gia_san_item.setText(_translate("MainWindow", self.format_value(stock_single['_fp_'])))

               # giá mở cửa _op_
               gia_mo_cua_item = QtWidgets.QTableWidgetItem()
               self.uic.tableWidget.setItem(row_index, COLUMN_NAME["open_value"]["index"], gia_mo_cua_item)
               gia_mo_cua_item.setText(_translate("MainWindow", self.format_value(stock_single['_op_'])))

