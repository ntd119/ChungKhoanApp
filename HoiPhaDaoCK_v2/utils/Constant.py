from PyQt5 import QtCore

VIETSTOCK_END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2"
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
MAX_MIN_END_POINT = "https://topchonlua.com/batch/data/stock_T0.json"
BACKGROUND_LO = "#F33232"
BACKGROUND_LAI = "#00E11A"
BACKGROUND_TRAN = "#860D98"
BACKGROUND_TANG = "#00E11A"
BACKGROUND_DUNG = "#FEA50C"
BACKGROUND_GIAM = "#F33232"
BACKGROUND_SAN = "#0A8AE3"
BACKGROUND_NONE = "#FFFFFF"
FILE_DA_MUA = "da_mua.json"
FILE_VN30 = "vn30.json"
FILE_VN100 = "vn100.json"
FILE_NGAN_HANG = "ngan_hang.json"
FILE_NANG_LUONG = "nang_luong.json"
FILE_SAN_XUAT = "san_xuat.json"
FILE_CONG_NGHE_THONG_TIN = "cong_nghe_thong_tin.json"
FILE_LUA_CHON_BOI_CAC_QUY = "chon_boi_quy.json"
FILE_QUY_ETF = "quy_etf.json"
FILE_CO_PHIEU_TRONG_KHOAN_10K = "cp_10k.json"
FILE_BAN_LE = "ban_le.json"
FILE_BAT_DONG_SAN = "bat_dong_san.json"
FILE_DUOC_PHAM_Y_TE = "duoc_pham_y_te.json"
FILE_TAI_CHINH = "tai_chinh.json"
FILE_TAI_NGUYEN = "tai_nguyen.json"
FILE_THUC_PHAM_VA_DO_UONG = "thuc_pham_va_do_uong.json"
FILE_VAN_TAI = "van_tai.json"
FILE_XAY_DUNG_VA_VAT_LIEU = "xay_dung_va_vat_lieu.json"
FILE_TAT_CA = "tat_ca.json"


NHOM_CO_PHIEU = {
    FILE_DA_MUA: {
        "name": "CP đã mua"
    },
    FILE_VN30: {
        "name": "VN30"
    },
    FILE_VN100: {
        "name": "VN100"
    },
    FILE_NGAN_HANG: {
        "name": "Ngân Hàng"
    },
    FILE_NANG_LUONG: {
        "name": "Năng lượng"
    },
    FILE_SAN_XUAT: {
        "name": "Sản xuất"
    },
    FILE_CONG_NGHE_THONG_TIN: {
        "name": "Công nghệ thông tin"
    },
    FILE_LUA_CHON_BOI_CAC_QUY: {
        "name": "Lựa chọn bởi các quỹ"
    },
    FILE_QUY_ETF: {
        "name": "Quỹ ETF"
    },
    FILE_CO_PHIEU_TRONG_KHOAN_10K: {
        "name": "Cổ phiếu trong khoản 10k"
    },
    FILE_BAN_LE: {
        "name": "Bán lẻ"
    },
    FILE_BAT_DONG_SAN: {
        "name": "Bất động sản"
    },
    FILE_DUOC_PHAM_Y_TE: {
        "name": "Dược phẩm & y tế"
    },
    FILE_TAI_CHINH: {
        "name": "Tài chính"
    },
    FILE_TAI_NGUYEN: {
        "name": "Tài nguyên"
    },
    FILE_THUC_PHAM_VA_DO_UONG: {
        "name": "Thực phẩm & đồ uống"
    },
    FILE_VAN_TAI: {
        "name": "Vận tải"
    },
    FILE_XAY_DUNG_VA_VAT_LIEU: {
        "name": "Xây dựng & vật liệu"
    },
    FILE_TAT_CA: {
        "name": "Tất cả"
    },
    "mot_nam_100": {
        "name": "Tăng >= 100% trong 1 năm"
    }
}

POSITION = {
    "nhom_co_phieu_label": {
        "geometry": QtCore.QRect(10, 10, 911, 31)
    },
    "search_input": {
        "geometry": QtCore.QRect(10, 50, 511, 31)
    },
    "phan_tram_thay_doi_trong_tuan": {
        "geometry": QtCore.QRect(10, 100, 511, 31)
    },
    "phan_tram_thay_doi_trong_tuan_value": {
        "geometry": QtCore.QRect(400, 100, 511, 31)
    },
    "button_thong_ke": {
        "geometry": QtCore.QRect(500, 100, 111, 31)
    },
    "table": {
        "geometry": QtCore.QRect(10, 150, 1440, 571)
    }
}

COLUMN_NAME = {
    "name": {
        "index": 0,
        "name": "Name"
    },
    "status": {
        "index": 1,
        "name": "Status"
    },
    "bought": {
        "index": 2,
        "name": "Giá mua"
    },
    "lai_lo": {
        "index": 3,
        "name": "Lãi/Lỗ"
    },
    "current_value": {
        "index": 4,
        "name": "Giá hiện tại"
    },
    "gia_ly_tuong": {
        "index": 5,
        "name": "Giá lý tưởng"
    },
    "gia_ht_so_gia_ly_tuong": {
        "index": 6,
        "name": "Giá HT so với \ngiá lý tưởng"
    },
    "percent_mong_cho": {
        "index": 7,
        "name": "% mong chờ"
    },
    "min_value_week": {
        "index": 8,
        "name": "Giá min \ntrong tuần"
    },
    "max_value_week": {
        "index": 9,
        "name": "Giá max \ntrong tuần"
    },
    "percent_max_min": {
        "index": 10,
        "name": "% Giá Max-Min"
    },
    "percent_max_current": {
        "index": 11,
        "name": "% Giá hiện tại\nso với giá max"
    },
    "min_time_week": {
        "index": 12,
        "name": "Min Time"
    },
    "max_time_week": {
        "index": 13,
        "name": "Max Time"
    },
    "percent_cut_loss": {
        "index": 14,
        "name": "% Cắt lỗ"
    },
    "percent_sell": {
        "index": 15,
        "name": "% Bán"
    },
    "tran_value": {
        "index": 16,
        "name": "Giá trần"
    },
    "san_value": {
        "index": 17,
        "name": "Giá sàn"
    },
    "open_value": {
        "index": 18,
        "name": "Giá mở cửa"
    },
    "has_infina": {
        "index": 19,
        "name": "Có trong\nInfina"
    }
}

THONG_KE_COLUM = {
    "changT0": {
        "index": 0,
        "file_index": 0,
        "name": "Giá hiện tại\nso với thứ 2-0"
    },
    "changT1": {
        "index": 1,
        "file_index": 1,
        "name": "Giá hiện tại\nso với thứ 2-1"
    },
    "changT2": {
        "index": 2,
        "file_index": 2,
        "name": "Giá hiện tại\nso với thứ 2-2"
    },
    "changT3": {
        "index": 3,
        "file_index": 3,
        "name": "Giá hiện tại\nso với thứ 2-3"
    },
    "changT4": {
        "index": 4,
        "file_index": 4,
        "name": "Giá hiện tại\nso với thứ 2-4"
    },
    "changT5": {
        "index": 5,
        "file_index": 5,
        "name": "Giá hiện tại\nso với thứ 2-5"
    },
    "changT6": {
        "index": 6,
        "file_index": 6,
        "name": "Giá hiện tại\nso với thứ 2-6"
    },
    "changT7": {
        "index": 7,
        "file_index": 7,
        "name": "Giá hiện tại\nso với thứ 2-7"
    },
    "changT8": {
        "index": 8,
        "file_index": 8,
        "name": "Giá hiện tại\nso với thứ 2-8"
    },
    "changT9": {
        "index": 9,
        "file_index": 9,
        "name": "Giá hiện tại\nso với thứ 2-9"
    },
    "changT10": {
        "index": 10,
        "file_index": 10,
        "name": "Giá hiện tại\nso với thứ 2-10"
    },
    "changT11": {
        "index": 11,
        "file_index": 11,
        "name": "Giá hiện tại\nso với thứ 2-11"
    },
    "changT12": {
        "index": 12,
        "file_index": 12,
        "name": "Giá hiện tại\nso với thứ 2-12"
    },
    "changT26": {
        "index": 13,
        "file_index": 26,
        "name": "Giá hiện tại\nso với 6-tháng"
    },
    "changT52": {
        "index": 14,
        "file_index": 52,
        "name": "Giá hiện tại\nso với 1-năm"
    },
    "changT51": {
        "index": 15,
        "file_index": 51,
        "name": "So với\n1-năm +1 tuần"
    },
    "changT104": {
        "index": 16,
        "file_index": 104,
        "name": "Giá hiện tại\nso với 2-năm"
    },
    "changT103": {
        "index": 17,
        "file_index": 103,
        "name": "So với\n2-năm +1 tuần"
    },
    "changT156": {
        "index": 18,
        "file_index": 156,
        "name": "Giá hiện tại\nso với 3-năm"
    },
    "changT155": {
        "index": 19,
        "file_index": 155,
        "name": "So với\n3-năm +1 tuần"
    },
    "changT208": {
        "index": 20,
        "file_index": 208,
        "name": "Giá hiện tại\nso với 4-năm"
    },
    "changT207": {
        "index": 21,
        "file_index": 207,
        "name": "So với\n4-năm +1 tuần"
    },
    "changT260": {
        "index": 22,
        "file_index": 260,
        "name": "Giá hiện tại\nso với 5-năm"
    },
    "changT259": {
        "index": 23,
        "file_index": 259,
        "name": "So với\n5-năm +1 tuần"
    }
}