# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1380, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.nhomCoPhieuLabel = QtWidgets.QLabel(self.centralwidget)
        self.nhomCoPhieuLabel.setGeometry(QtCore.QRect(10, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.nhomCoPhieuLabel.setFont(font)
        self.nhomCoPhieuLabel.setObjectName("nhomCoPhieuLabel")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 256, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
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
        self.menuVn = QtWidgets.QAction(MainWindow)
        self.menuVn.setObjectName("menuVn")
        self.actionNganHang = QtWidgets.QAction(MainWindow)
        self.actionNganHang.setObjectName("actionNganHang")
        self.actionNangLuong = QtWidgets.QAction(MainWindow)
        self.actionNangLuong.setObjectName("actionNangLuong")
        self.actionSanXuat = QtWidgets.QAction(MainWindow)
        self.actionSanXuat.setObjectName("actionS_n_xu_t")
        self.menuNhonCoPhieu.addAction(self.menuDaMua)
        self.menuNhonCoPhieu.addAction(self.menuVn)
        self.menuNhonCoPhieu.addAction(self.actionNganHang)
        self.menuNhonCoPhieu.addAction(self.actionNangLuong)
        self.menuNhonCoPhieu.addAction(self.actionSanXuat)
        self.menubar.addAction(self.menuNhonCoPhieu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.nhomCoPhieuLabel.setText(_translate("MainWindow", "Nhóm cổ phiếu: "))
        self.menuNhonCoPhieu.setTitle(_translate("MainWindow", "Nhóm cổ phiếu"))
        self.menuDaMua.setText(_translate("MainWindow", "Cổ phiếu đã mua"))
        self.menuDaMua.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.menuVn.setText(_translate("MainWindow", "VN100"))
        self.menuVn.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionNganHang.setText(_translate("MainWindow", "Ngân hàng"))
        self.actionNganHang.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionNangLuong.setText(_translate("MainWindow", "Năng lượng"))
        self.actionNangLuong.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionSanXuat.setText(_translate("MainWindow", "Sản xuất"))
        self.actionSanXuat.setShortcut(_translate("MainWindow", "Ctrl+S"))
