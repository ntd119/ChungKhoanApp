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
        self.data_max_min = self.call_api_max_min()
        self.show_table()

    def call_api_max_min(self):
        try:
            response = requests.get(MAX_MIN_END_POINT, headers=HEADERS)
            return response.json()
        except:
            print("Max min api error")
            time.sleep(5)
            self.call_api_max_min()

    def show_table(self):
        nhom_nganh = []
        for nganh in NHOM_CO_PHIEU:
            if nganh == FILE_DA_MUA or nganh == FILE_VN30 or nganh == FILE_VN100  or nganh == FILE_TAT_CA:
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
        for i in range(1):
            item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(_translate("MainWindow", "Phần trăm\nthay đổi\ntrong tuần"))

        # set tên dòng
        for row_index, ten_nganh in enumerate(nhom_nganh):
            item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setVerticalHeaderItem(row_index, item)
            item.setText(_translate("MainWindow", ten_nganh["name"]))

        for row_index, nganh in enumerate(nhom_nganh):
            file_name = nganh["file"]
            percent = self.tinh_phan_tram_thay_doi(file_name)
            item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setItem(row_index, 0, item)
            item.setText(_translate("MainWindow", self.format_2_decimal(percent) + "%"))
            if percent < 0:
                self.uic.tableWidget.item(row_index, 0).setBackground(
                    QtGui.QColor(BACKGROUND_LO))
            else:
                self.uic.tableWidget.item(row_index, 0).setBackground(
                    QtGui.QColor(BACKGROUND_LAI))


    def format_2_decimal(self, value):
        return "{:.2f}".format(value)

    def tinh_phan_tram_thay_doi(self, file_name):
        _translate = QtCore.QCoreApplication.translate
        sum_head_price = 0
        sum_tail_price = 0
        with open(f"data/{file_name}", "r") as file_data:
            data_from_file = json.load(file_data)
            for row_index, stock_code in enumerate(data_from_file):
                try:
                    max_min_dict = self.data_max_min[stock_code]
                except KeyError:
                    continue
                sum_head_price += max_min_dict["head_price"]
                sum_tail_price += max_min_dict["tail_price"]
            try:
                percent = ((sum_tail_price - sum_head_price) / sum_head_price) * 100
            except:
                percent = 0
            return percent
