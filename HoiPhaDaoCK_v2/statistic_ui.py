import time
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui
from statistic_form import Ui_Dialog
import requests
import json
from utils.Constant import *


class StatisticUI:
    def __init__(self):
        self.window = QMainWindow()
        self.uic = Ui_Dialog()
        self.uic.setupUi(self.window)
        self.window.show()
        self.data_vietstock = self.call_api_vietstock()
        self.data_max_min_0 = self.call_api_max_min(0)
        self.data_max_min_1 = self.call_api_max_min(1)
        self.data_max_min_2 = self.call_api_max_min(2)
        self.data_max_min_3 = self.call_api_max_min(3)
        self.show_table()

    def call_api_max_min(self, index_file):
        try:
            response = requests.get(f"https://topchonlua.com/batch/data/stock_T{index_file}.json", headers=HEADERS)
            return response.json()
        except:
            print("Max min api error")
            time.sleep(5)
            self.call_api_max_min(index_file)

    def call_api_vietstock(self):
        vietstock_prams = {
            "sectorID": 0,
            "catID": 0,
            "capitalID": 0,
            "languageID": 1
        }
        try:
            response = requests.get(VIETSTOCK_END_POINT, params=vietstock_prams, headers=HEADERS)
            return response.json()
        except:
            print("Call vietstock error")
            time.sleep(5)
            self.call_api_vietstock()

    def show_table(self):
        nhom_nganh = []
        for nganh in NHOM_CO_PHIEU:
            if nganh == FILE_DA_MUA or nganh == FILE_VN30 or nganh == FILE_VN100 or nganh == FILE_TAT_CA:
                continue
            dict_item = {
                "name": NHOM_CO_PHIEU[nganh]["name"],
                "file": nganh
            }
            nhom_nganh.append(dict_item)
        self.uic.tableWidget.setRowCount(len(nhom_nganh))
        self.uic.tableWidget.setColumnCount(5)
        _translate = QtCore.QCoreApplication.translate

        # set tên cột
        for i in range(4):
            item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(_translate("MainWindow", f"Giá hiện tại\nso với thứ 2\n{i}"))

        # set tên dòng
        for row_index, ten_nganh in enumerate(nhom_nganh):
            item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setVerticalHeaderItem(row_index, item)
            item.setText(_translate("MainWindow", ten_nganh["name"]))

        for colum_index in range(4):
            for row_index, nganh in enumerate(nhom_nganh):
                file_name = nganh["file"]
                percent = self.tinh_phan_tram_thay_doi(file_name, colum_index)
                item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, colum_index, item)
                item.setText(_translate("MainWindow", self.format_2_decimal(percent) + "%"))
                if percent < 0:
                    self.uic.tableWidget.item(row_index, colum_index).setBackground(
                        QtGui.QColor(BACKGROUND_LO))
                else:
                    self.uic.tableWidget.item(row_index, colum_index).setBackground(
                        QtGui.QColor(BACKGROUND_LAI))

    def format_2_decimal(self, value):
        return "{:.2f}".format(value)

    def tinh_phan_tram_thay_doi(self, file_name, index_file):
        _translate = QtCore.QCoreApplication.translate
        sum_head_price = 0
        sum_tail_price = 0

        with open(f"data/{file_name}", "r") as file_data:
            data_from_file = json.load(file_data)
            for row_index, stock_code in enumerate(data_from_file):
                try:
                    if index_file == 0:
                        max_min_dict = self.data_max_min_0[stock_code]
                    elif index_file == 1:
                        max_min_dict = self.data_max_min_1[stock_code]
                    elif index_file == 2:
                        max_min_dict = self.data_max_min_2[stock_code]
                    elif index_file == 3:
                        max_min_dict = self.data_max_min_3[stock_code]
                except KeyError:
                    continue
                sum_head_price += max_min_dict["head_price"]
                stock_single = [row for row in self.data_vietstock if row["_sc_"] == stock_code.upper()]
                if len(stock_single) == 1:
                    stock_single = stock_single[0]
                    sum_tail_price += stock_single['_cp_']
            try:
                percent = ((sum_tail_price - sum_head_price) / sum_head_price) * 100
            except:
                percent = 0
            return percent
