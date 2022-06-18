# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from utils.Constant import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1480, 790)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.nhomCoPhieuLabel = QtWidgets.QLabel(self.centralwidget)
        self.nhomCoPhieuLabel.setObjectName("nhomCoPhieuLabel")

        self.phanTramThayDoiTrongTuanLabel = QtWidgets.QLabel(self.centralwidget)
        self.phanTramThayDoiTrongTuanLabel.setObjectName("phanTramThayDoiTrongTuanLabel")

        self.phanTramThayDoiTrongTuanValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.phanTramThayDoiTrongTuanValueLabel.setObjectName("phanTramThayDoiTrongTuanValueLabel")

        self.searchInput = QtWidgets.QLineEdit(self.centralwidget)
        self.searchInput.setObjectName("searchInput")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 485, 18))
        self.menubar.setObjectName("menubar")
        self.menuNhonCoPhieu = QtWidgets.QMenu(self.menubar)
        self.menuNhonCoPhieu.setObjectName("menuNhonCoPhieu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuDaMua = QtWidgets.QAction(MainWindow)
        self.menuDaMua.setObjectName("menuDaMua")
        self.menuVn100 = QtWidgets.QAction(MainWindow)
        self.menuVn100.setObjectName("menuVn")
        # vn30
        self.menuVn30 = QtWidgets.QAction(MainWindow)
        self.menuVn30.setObjectName("menuVn30")
        self.menuNganHang = QtWidgets.QAction(MainWindow)
        self.menuNganHang.setObjectName("menuNganHang")
        self.menuNangLuong = QtWidgets.QAction(MainWindow)
        self.menuNangLuong.setObjectName("menuNangLuong")
        self.menuSanXuat = QtWidgets.QAction(MainWindow)
        self.menuSanXuat.setObjectName("menuSanXuat")
        self.menuCongNgheThongTin = QtWidgets.QAction(MainWindow)
        self.menuCongNgheThongTin.setObjectName("menuCongNgheThongTin")
        self.menuLuaChonBoiCacQuy = QtWidgets.QAction(MainWindow)
        self.menuLuaChonBoiCacQuy.setObjectName("menuLuaChonBoiCacQuy")
        self.menuQuyETF = QtWidgets.QAction(MainWindow)
        self.menuQuyETF.setObjectName("menuQuyETF")

        # Cổ phiếu trong khoản 10k
        self.menuCoPhieuTrongKhoan10k = QtWidgets.QAction(MainWindow)
        self.menuCoPhieuTrongKhoan10k.setObjectName("menuCoPhieuTrongKhoan10k")

        # Bán lẻ
        self.menuBanLe = QtWidgets.QAction(MainWindow)
        self.menuBanLe.setObjectName("menuBanLe")

        # Bất động sản
        self.menuBatDongSan = QtWidgets.QAction(MainWindow)
        self.menuBatDongSan.setObjectName("menuBatDongSan")

        # Dược phẩm và y tế
        self.menuDuocPhamVaYte = QtWidgets.QAction(MainWindow)
        self.menuDuocPhamVaYte.setObjectName("menuDuocPhamVaYte")

        # Tài chính
        self.menuTaiChinh = QtWidgets.QAction(MainWindow)
        self.menuTaiChinh.setObjectName("menuTaiChinh")

        # Tài nguyên
        self.menuTaiNguyen = QtWidgets.QAction(MainWindow)
        self.menuTaiNguyen.setObjectName("menuTaiNguyen")

        # Thực phẩm & đồ uống
        self.menuThucPhamVaDoUong = QtWidgets.QAction(MainWindow)
        self.menuThucPhamVaDoUong.setObjectName("menuThucPhamVaDoUong")

        # Vận tải
        self.menuVanTai = QtWidgets.QAction(MainWindow)
        self.menuVanTai.setObjectName("menuVanTai")

        # Xây dựng & vật liệu
        self.menuXayDungVaVatLieu = QtWidgets.QAction(MainWindow)
        self.menuXayDungVaVatLieu.setObjectName("menuXayDungVaVatLieu")

        # Tất cả
        self.menuTatCa = QtWidgets.QAction(MainWindow)
        self.menuTatCa.setObjectName("menuTatCa")

        self.menuNhonCoPhieu.addAction(self.menuDaMua)
        self.menuNhonCoPhieu.addAction(self.menuVn30)
        self.menuNhonCoPhieu.addAction(self.menuVn100)
        self.menuNhonCoPhieu.addAction(self.menuNganHang)
        self.menuNhonCoPhieu.addAction(self.menuNangLuong)
        self.menuNhonCoPhieu.addAction(self.menuSanXuat)
        self.menuNhonCoPhieu.addAction(self.menuCongNgheThongTin)
        self.menuNhonCoPhieu.addAction(self.menuLuaChonBoiCacQuy)
        self.menuNhonCoPhieu.addAction(self.menuQuyETF)
        self.menuNhonCoPhieu.addAction(self.menuCoPhieuTrongKhoan10k)
        self.menuNhonCoPhieu.addAction(self.menuBanLe)
        self.menuNhonCoPhieu.addAction(self.menuBatDongSan)
        self.menuNhonCoPhieu.addAction(self.menuDuocPhamVaYte)
        self.menuNhonCoPhieu.addAction(self.menuTaiChinh)
        self.menuNhonCoPhieu.addAction(self.menuTaiNguyen)
        self.menuNhonCoPhieu.addAction(self.menuThucPhamVaDoUong)
        self.menuNhonCoPhieu.addAction(self.menuVanTai)
        self.menuNhonCoPhieu.addAction(self.menuXayDungVaVatLieu)
        self.menuNhonCoPhieu.addAction(self.menuTatCa)
        self.menubar.addAction(self.menuNhonCoPhieu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuNhonCoPhieu.setTitle(_translate("MainWindow", "Chọn cổ phiếu"))
        self.menuDaMua.setText(_translate("MainWindow", "Cổ phiếu đã mua"))
        self.menuDaMua.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.menuVn30.setText(_translate("MainWindow", NHOM_CO_PHIEU[FILE_VN30]["name"]))
        self.menuVn100.setText(_translate("MainWindow", "VN100"))
        self.menuVn100.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.menuNganHang.setText(_translate("MainWindow", "Ngân hàng"))
        self.menuNganHang.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.menuNangLuong.setText(_translate("MainWindow", "Năng lượng"))
        self.menuNangLuong.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.menuSanXuat.setText(_translate("MainWindow", "Sản xuất"))
        self.menuSanXuat.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.menuCongNgheThongTin.setText(_translate("MainWindow", "CNTT"))
        self.menuCongNgheThongTin.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.menuLuaChonBoiCacQuy.setText(_translate("MainWindow", "Lựa chọn bởi các quỹ"))
        self.menuLuaChonBoiCacQuy.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.menuQuyETF.setText(_translate("MainWindow", NHOM_CO_PHIEU[FILE_QUY_ETF]["name"]))
        self.menuCoPhieuTrongKhoan10k.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_CO_PHIEU_TRONG_KHOAN_10K]["name"]))
        self.menuBanLe.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_BAN_LE]["name"]))
        self.menuBatDongSan.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_BAT_DONG_SAN]["name"]))
        self.menuDuocPhamVaYte.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_DUOC_PHAM_Y_TE]["name"]))
        self.menuTaiChinh.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_TAI_CHINH]["name"]))
        self.menuTaiNguyen.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_TAI_NGUYEN]["name"]))
        self.menuThucPhamVaDoUong.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_THUC_PHAM_VA_DO_UONG]["name"]))
        self.menuVanTai.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_VAN_TAI]["name"]))
        self.menuXayDungVaVatLieu.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_XAY_DUNG_VA_VAT_LIEU]["name"]))
        self.menuTatCa.setText(
            _translate("MainWindow", NHOM_CO_PHIEU[FILE_TAT_CA]["name"]))
