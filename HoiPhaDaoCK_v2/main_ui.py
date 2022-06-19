import time

from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui
from qt_form import Ui_MainWindow
from statistic_form import Ui_Dialog
from statistic_ui import StatisticUI

import requests
import json
from datetime import datetime
from utils.Constant import *
import unidecode


class MainUI:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.head_sum = 0
        self.current_sum = 0
        self.data_vietstock = None
        self.data_max_min = None
        self.data_from_file = None
        self.setPositon()
        self.data_qua_khu = self.lay_du_lieu_qua_khu()
        self.run(FILE_VN100)
        self.write_to_all_file()
        self.event_on()

    def setPositon(self):
        self.uic.tableWidget.setGeometry(POSITION["table"]["geometry"])
        self.uic.nhomCoPhieuLabel.setGeometry(POSITION["nhom_co_phieu_label"]["geometry"])
        self.uic.thongKeButton.setGeometry(POSITION["button_thong_ke"]["geometry"])
        self.uic.thongKeButton.setText("Thống kê")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.uic.nhomCoPhieuLabel.setFont(font)

        # Phần trăm thay đổi trong tuần
        self.uic.phanTramThayDoiTrongTuanLabel.setGeometry(POSITION["phan_tram_thay_doi_trong_tuan"]["geometry"])
        self.uic.phanTramThayDoiTrongTuanLabel.setText("Phần trăm thay đổi trong tuần: ")
        self.uic.phanTramThayDoiTrongTuanLabel.setFont(font)

        # Giá trị phần trăm thay đổi trong tuần
        self.uic.phanTramThayDoiTrongTuanValueLabel.setGeometry(POSITION["phan_tram_thay_doi_trong_tuan_value"]["geometry"])
        self.uic.phanTramThayDoiTrongTuanValueLabel.setText(self.format_2_decimal(0) + "%")
        self.uic.phanTramThayDoiTrongTuanValueLabel.setFont(font)
        self.uic.phanTramThayDoiTrongTuanValueLabel.setStyleSheet(f'color: {BACKGROUND_LAI}')

        # textbox tìm kiếm
        self.uic.searchInput.setFixedWidth(300)
        self.uic.searchInput.setPlaceholderText("Tìm kiếm theo mã hoặc tên CK")
        self.uic.searchInput.setToolTip("Không cần nhập có dấu")
        self.uic.searchInput.setGeometry(POSITION["search_input"]["geometry"])

    def chang_in_week(self):
        _translate = QtCore.QCoreApplication.translate
        for row_index, stock_code in enumerate(self.data_from_file):
            for column_index in range(COLUMN_NUMBER_THONG_KE + 1):
                try:
                    max_min_dict = self.data_qua_khu[column_index][stock_code]
                except KeyError:
                    continue
                head_price = max_min_dict["head_price"]
                tail_price = 0
                stock_single = [row for row in self.data_vietstock if row["_sc_"] == stock_code.upper()]
                if len(stock_single) == 1:
                    stock_single = stock_single[0]
                    tail_price += stock_single['_cp_']
                try:
                    percent = ((tail_price - head_price) / head_price) * 100
                except:
                    percent = 0
                item_bought = QtWidgets.QTableWidgetItem()
                index = COLUMN_NAME[f"changT{column_index}"]["index"]
                self.uic.tableWidget.setItem(row_index, index, item_bought)
                item_bought.setText(_translate("MainWindow", self.format_2_decimal(percent) + "%"))
                if percent < 0:
                    self.uic.tableWidget.item(row_index, index).setBackground(
                        QtGui.QColor(BACKGROUND_LO))
                else:
                    self.uic.tableWidget.item(row_index, index).setBackground(
                    QtGui.QColor(BACKGROUND_LAI))


    def event_on(self):
        self.uic.thongKeButton.clicked.connect(self.show_statistic_form)
        self.uic.searchInput.textChanged.connect(self.search_on_table)
        self.uic.menuDaMua.triggered.connect(lambda: self.run(FILE_DA_MUA))
        self.uic.menuVn30.triggered.connect(lambda: self.run(FILE_VN30))
        self.uic.menuNganHang.triggered.connect(lambda: self.run(FILE_NGAN_HANG))
        self.uic.menuVn100.triggered.connect(lambda: self.run(FILE_VN100))
        self.uic.menuNangLuong.triggered.connect(lambda: self.run(FILE_NANG_LUONG))
        self.uic.menuSanXuat.triggered.connect(lambda: self.run(FILE_SAN_XUAT))
        self.uic.menuCongNgheThongTin.triggered.connect(lambda: self.run(FILE_CONG_NGHE_THONG_TIN))
        self.uic.menuLuaChonBoiCacQuy.triggered.connect(lambda: self.run(FILE_LUA_CHON_BOI_CAC_QUY))
        self.uic.menuQuyETF.triggered.connect(lambda: self.run(FILE_QUY_ETF))
        self.uic.menuCoPhieuTrongKhoan10k.triggered.connect(lambda: self.run(FILE_CO_PHIEU_TRONG_KHOAN_10K))
        self.uic.menuBanLe.triggered.connect(lambda: self.run(FILE_BAN_LE))
        self.uic.menuBatDongSan.triggered.connect(lambda: self.run(FILE_BAT_DONG_SAN))
        self.uic.menuDuocPhamVaYte.triggered.connect(lambda: self.run(FILE_DUOC_PHAM_Y_TE))
        self.uic.menuTaiChinh.triggered.connect(lambda: self.run(FILE_TAI_CHINH))
        self.uic.menuTaiNguyen.triggered.connect(lambda: self.run(FILE_TAI_NGUYEN))
        self.uic.menuThucPhamVaDoUong.triggered.connect(lambda: self.run(FILE_THUC_PHAM_VA_DO_UONG))
        self.uic.menuVanTai.triggered.connect(lambda: self.run(FILE_VAN_TAI))
        self.uic.menuXayDungVaVatLieu.triggered.connect(lambda: self.run(FILE_XAY_DUNG_VA_VAT_LIEU))
        self.uic.menuTatCa.triggered.connect(lambda: self.run(FILE_TAT_CA))

    def show_statistic_form(self):
        self.statisticUI = StatisticUI(self.data_qua_khu)

    def write_to_all_file(self):
        with open("data/tat_ca.json", 'r') as data_file:
            data_from_file = json.load(data_file)
        with open("data/tat_ca.json", 'w') as stock_file:
            for item in self.data_vietstock:
                stock = {
                    item["_sc_"]: {
                        "should_buy": 0,
                        "enable_sound": 0,
                        "bought": 0,
                        "percent_cut_loss": "4.0",
                        "percent_sell": "4.0",
                        "follow": 0
                    }
                }
                data_from_file.update(stock)
            json.dump(data_from_file, stock_file, indent=4)

    def search_on_table(self):
        searching = self.remove_dau_tieng_viet(self.uic.searchInput.text().lower())
        for row in range(self.uic.tableWidget.rowCount()):
            stock_code = self.remove_dau_tieng_viet(self.uic.tableWidget.verticalHeaderItem(row).text().lower())
            name = self.remove_dau_tieng_viet(self.uic.tableWidget.item(row, 0).text().lower())
            self.uic.tableWidget.setRowHidden(row, (
                    searching not in stock_code and searching not in name))

    def remove_dau_tieng_viet(self, accented_string):
        return unidecode.unidecode(accented_string)

    def run(self, file_name):
        self.uic.searchInput.clear()
        self.update_title(file_name)
        self.draw_table(file_name)
        self.update_max_min()
        self.update_table()
        self.chang_in_week()

    def update_title(self, file_name):
        title = "Nhóm cổ phiếu: " + NHOM_CO_PHIEU[file_name]["name"]
        self.uic.nhomCoPhieuLabel.setText(title)

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

    def format_2_decimal(self, value):
        return "{:.2f}".format(value)

    def draw_table(self, file_name):
        self.uic.tableWidget.clear()
        with open(f"data/{file_name}") as file_data:
            self.data_from_file = json.load(file_data)
            self.data_from_file = dict(
                sorted(self.data_from_file.items(), key=lambda item: item[1]["follow"], reverse=True))
            row_number = len(self.data_from_file)
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
        self.current_sum = 0
        now = datetime.now().time()
        format_time = now.strftime("%H:%M:%S")
        print(f"Update gia co phieu... {format_time}")
        self.call_api_vietstock()
        _translate = QtCore.QCoreApplication.translate
        for row_index, stock_code in enumerate(self.data_from_file):
            stock_single = [row for row in self.data_vietstock if row["_sc_"] == stock_code.upper()]
            if len(stock_single) == 1:
                stock_single = stock_single[0]

                # Tên cổ phiếu
                stock_name_value = stock_single['stockName']
                stock_name_item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["name"]["index"], stock_name_item)
                stock_name_item.setText(_translate("MainWindow", str(stock_name_value)))

                # giá trần _clp_
                gia_tran_value = stock_single['_clp_']
                gia_tran_item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["tran_value"]["index"], gia_tran_item)
                gia_tran_item.setText(_translate("MainWindow", self.format_value(gia_tran_value)))

                # giá sàn _fp_
                gia_san_value = stock_single['_fp_']
                gia_san_item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["san_value"]["index"], gia_san_item)
                gia_san_item.setText(_translate("MainWindow", self.format_value(gia_san_value)))

                # giá mở cửa _op_
                gia_mo_cua_value = stock_single['_op_']
                gia_mo_cua_item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["open_value"]["index"], gia_mo_cua_item)
                gia_mo_cua_item.setText(_translate("MainWindow", self.format_value(gia_mo_cua_value)))

                # giá hiện tại _cp_
                gia_hien_tai_value = stock_single['_cp_']
                self.current_sum += gia_hien_tai_value
                percent = stock_single['_pc_']
                gia_hien_tai_item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["current_value"]["index"], gia_hien_tai_item)
                gia_hien_tai_item.setText(
                    _translate("MainWindow",
                               self.format_value(gia_hien_tai_value) + " (" + self.format_2_decimal(percent) + "%)"))
                # Giá tham chiếu _bp_
                gia_tham_chieu_value = stock_single['_bp_']
                if gia_hien_tai_value == gia_tran_value:
                    self.uic.tableWidget.item(row_index, COLUMN_NAME["current_value"]["index"]).setBackground(
                        QtGui.QColor(BACKGROUND_TRAN))
                elif gia_hien_tai_value == gia_san_value:
                    self.uic.tableWidget.item(row_index, COLUMN_NAME["current_value"]["index"]).setBackground(
                        QtGui.QColor(BACKGROUND_SAN))
                elif gia_hien_tai_value == gia_tham_chieu_value:
                    self.uic.tableWidget.item(row_index, COLUMN_NAME["current_value"]["index"]).setBackground(
                        QtGui.QColor(BACKGROUND_DUNG))
                elif percent >= 0:
                    self.uic.tableWidget.item(row_index, COLUMN_NAME["current_value"]["index"]).setBackground(
                        QtGui.QColor(BACKGROUND_TANG))
                else:
                    self.uic.tableWidget.item(row_index, COLUMN_NAME["current_value"]["index"]).setBackground(
                        QtGui.QColor(BACKGROUND_GIAM))

                # Tính lãi lỗ
                gia_da_mua = self.uic.tableWidget.item(row_index, COLUMN_NAME["bought"]["index"]).text()
                if len(gia_da_mua) > 0:
                    try:
                        gia_da_mua = int(gia_da_mua)
                        percent_lai_lo = ((gia_hien_tai_value - gia_da_mua) / gia_da_mua) * 100
                    except:
                        gia_da_mua = 0
                        percent_lai_lo = 0
                    percen_lai_lo_item = QtWidgets.QTableWidgetItem()
                    self.uic.tableWidget.setItem(row_index, COLUMN_NAME["lai_lo"]["index"], percen_lai_lo_item)
                    percen_lai_lo_item.setText(_translate("MainWindow", self.format_2_decimal(percent_lai_lo) + "%"))
                    if percent_lai_lo < 0:
                        self.uic.tableWidget.item(row_index, COLUMN_NAME["lai_lo"]["index"]).setBackground(
                            QtGui.QColor(BACKGROUND_LO))
                    else:
                        self.uic.tableWidget.item(row_index, COLUMN_NAME["lai_lo"]["index"]).setBackground(
                            QtGui.QColor(BACKGROUND_LAI))

                    # Status
                    percent_cat_lo = self.uic.tableWidget.item(row_index,
                                                               COLUMN_NAME["percent_cut_loss"]["index"]).text()
                    percent_ban = self.uic.tableWidget.item(row_index, COLUMN_NAME["percent_sell"]["index"]).text()
                    status_ban_item = QtWidgets.QTableWidgetItem()
                    self.uic.tableWidget.setItem(row_index, COLUMN_NAME["status"]["index"],
                                                 status_ban_item)
                    self.uic.tableWidget.item(row_index, COLUMN_NAME["status"]["index"]).setBackground(
                        QtGui.QColor(BACKGROUND_NONE))
                    if percent_lai_lo >= 0:
                        if float(percent_lai_lo) >= float(percent_ban):
                            status_ban_item.setText(_translate("MainWindow", "Bán"))
                            self.uic.tableWidget.item(row_index, COLUMN_NAME["status"]["index"]).setBackground(
                                QtGui.QColor(BACKGROUND_LAI))
                    else:
                        if abs(float(percent_lai_lo)) >= float(percent_cat_lo):
                            status_cat_lo_item = QtWidgets.QTableWidgetItem()
                            self.uic.tableWidget.setItem(row_index, COLUMN_NAME["status"]["index"],
                                                         status_cat_lo_item)
                            status_cat_lo_item.setText(_translate("MainWindow", "Cắt lỗ"))
                            self.uic.tableWidget.item(row_index, COLUMN_NAME["status"]["index"]).setBackground(
                                QtGui.QColor(BACKGROUND_LO))
                # Phần trăm giá max so với hiện tại
                try:
                    gia_max_this_week = self.uic.tableWidget.item(row_index, COLUMN_NAME["max_value_week"]["index"]).text()
                    gia_max_this_week = gia_max_this_week.replace(',', '')
                    percent_max_current_value = ((float(gia_hien_tai_value) - float(gia_max_this_week)) / float(
                        gia_max_this_week)) * 100
                except:
                    pass
                percent_max_current_item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["percent_max_current"]["index"],
                                             percent_max_current_item)
                percent_max_current_item.setText(
                    _translate("MainWindow", self.format_2_decimal(percent_max_current_value)))
                if percent_max_current_value >= 0:
                    self.uic.tableWidget.item(row_index, COLUMN_NAME["percent_max_current"]["index"]).setBackground(
                        QtGui.QColor(BACKGROUND_LAI))
                else:
                    self.uic.tableWidget.item(row_index, COLUMN_NAME["percent_max_current"]["index"]).setBackground(
                        QtGui.QColor(BACKGROUND_LO))
            else:
                stock_name_item = QtWidgets.QTableWidgetItem()
                self.uic.tableWidget.setItem(row_index, COLUMN_NAME["name"]["index"], stock_name_item)
                stock_name_item.setText(_translate("MainWindow", "Mã ck không tồn tại"))
                self.uic.tableWidget.item(row_index, COLUMN_NAME["name"]["index"]).setBackground(
                    QtGui.QColor(BACKGROUND_LO))

        # Set phần trăm thay đổi trong tuần
        percent_sum = ((self.current_sum - self.head_sum) / self.head_sum) * 100
        color_sum = BACKGROUND_LAI
        if percent_sum < 0:
            color_sum = BACKGROUND_LO
        self.uic.phanTramThayDoiTrongTuanValueLabel.setText(self.format_2_decimal(percent_sum) + "%")
        self.uic.phanTramThayDoiTrongTuanValueLabel.setStyleSheet(f'color: {color_sum}')

    def call_api_max_min(self):
        try:
            response = requests.get(MAX_MIN_END_POINT, headers=HEADERS)
            self.data_max_min = response.json()
        except:
            print("Max min api error")
            time.sleep(5)
            self.call_api_max_min()

    def format_time(self, time_value):
        date = datetime.fromtimestamp(time_value / 1000.0)
        day_of_week = int(date.strftime("%w")) + 1
        return date.strftime(f"T{day_of_week}, %d-%m, %I:%M %p")

    def update_max_min(self):
        print("Update gia max min")
        self.head_sum = 0
        self.call_api_max_min()
        _translate = QtCore.QCoreApplication.translate
        for row_index, stock_code in enumerate(self.data_from_file):
            try:
                max_min_dict = self.data_max_min[stock_code]
            except KeyError:
                continue
            self.head_sum += max_min_dict["head_price"]
            # giá min tuần này
            min_value = max_min_dict["min_price"]
            gia_min_this_week_item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setItem(row_index, COLUMN_NAME["min_value_week"]["index"], gia_min_this_week_item)
            gia_min_this_week_item.setText(_translate("MainWindow", self.format_value(min_value)))

            # Thời gian giá nhỏ nhất tuần này
            min_time_this_week_item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setItem(row_index, COLUMN_NAME["min_time_week"]["index"], min_time_this_week_item)
            min_time_this_week_item.setText(_translate("MainWindow", self.format_time(max_min_dict["min_price_time"])))

            # giá max tuần này
            max_value = max_min_dict["max_price"]
            gia_max_this_week_item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setItem(row_index, COLUMN_NAME["max_value_week"]["index"], gia_max_this_week_item)
            gia_max_this_week_item.setText(_translate("MainWindow", self.format_value(max_value)))

            # Thời gian giá lớn nhất tuần này
            max_time_this_week_item = QtWidgets.QTableWidgetItem()
            self.uic.tableWidget.setItem(row_index, COLUMN_NAME["max_time_week"]["index"], max_time_this_week_item)
            max_time_this_week_item.setText(_translate("MainWindow", self.format_time(max_min_dict["max_price_time"])))

            # Phần trăm max min
            percent_max_min_this_week_item = QtWidgets.QTableWidgetItem()
            percent_max_min = ((max_value - min_value) / min_value) * 100
            self.uic.tableWidget.setItem(row_index, COLUMN_NAME["percent_max_min"]["index"],
                                         percent_max_min_this_week_item)
            percent_max_min_this_week_item.setText(_translate("MainWindow", self.format_2_decimal(percent_max_min)))
            if percent_max_min >= 0:
                self.uic.tableWidget.item(row_index, COLUMN_NAME["percent_max_min"]["index"]).setBackground(
                    QtGui.QColor(BACKGROUND_LAI))
            else:
                self.uic.tableWidget.item(row_index, COLUMN_NAME["percent_max_min"]["index"]).setBackground(
                    QtGui.QColor(BACKGROUND_LO))

    def lay_du_lieu_qua_khu(self):
        qua_khu_data = {}
        for tuan in range(COLUMN_NUMBER_THONG_KE + 1):
            reponse = self.call_api_max_min_thong_ke(tuan)
            qua_khu_data[tuan] = reponse
        return qua_khu_data

    def call_api_max_min_thong_ke(self, index_file):
        try:
            response = requests.get(f"https://topchonlua.com/batch/data/stock_T{index_file}.json", headers=HEADERS)
            return response.json()
        except:
            print("Max min api error")
            time.sleep(5)
            self.call_api_max_min_thong_ke(index_file)