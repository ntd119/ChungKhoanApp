from PyQt5 import QtCore

FIREANT_URL = "https://restv2.fireant.vn/"
FIREANT_AUTH = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxODg5NjIyNTMwLCJuYmYiOjE1ODk2MjI1MzAsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsiYWNhZGVteS1yZWFkIiwiYWNhZGVteS13cml0ZSIsImFjY291bnRzLXJlYWQiLCJhY2NvdW50cy13cml0ZSIsImJsb2ctcmVhZCIsImNvbXBhbmllcy1yZWFkIiwiZmluYW5jZS1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImludmVzdG9wZWRpYS1yZWFkIiwib3JkZXJzLXJlYWQiLCJvcmRlcnMtd3JpdGUiLCJwb3N0cy1yZWFkIiwicG9zdHMtd3JpdGUiLCJzZWFyY2giLCJzeW1ib2xzLXJlYWQiLCJ1c2VyLWRhdGEtcmVhZCIsInVzZXItZGF0YS13cml0ZSIsInVzZXJzLXJlYWQiXSwianRpIjoiMjYxYTZhYWQ2MTQ5Njk1ZmJiYzcwODM5MjM0Njc1NWQifQ.dA5-HVzWv-BRfEiAd24uNBiBxASO-PAyWeWESovZm_hj4aXMAZA1-bWNZeXt88dqogo18AwpDQ-h6gefLPdZSFrG5umC1dVWaeYvUnGm62g4XS29fj6p01dhKNNqrsu5KrhnhdnKYVv9VdmbmqDfWR8wDgglk5cJFqalzq6dJWJInFQEPmUs9BW_Zs8tQDn-i5r4tYq2U8vCdqptXoM7YgPllXaPVDeccC9QNu2Xlp9WUvoROzoQXg25lFub1IYkTrM66gJ6t9fJRZToewCt495WNEOQFa_rwLCZ1QwzvL0iYkONHS_jZ0BOhBCdW9dWSawD6iF1SIQaFROvMDH1rg"


VIETSTOCK_END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2"
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           'Authorization': FIREANT_AUTH
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
    }
}

POSITION = {
    "nhom_co_phieu_label": {
        "geometry": QtCore.QRect(10, 10, 511, 31)
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
    "min_value_week": {
        "index": 5,
        "name": "Giá min \ntrong tuần"
    },
    "max_value_week": {
        "index": 6,
        "name": "Giá max \ntrong tuần"
    },
    "percent_max_min": {
        "index": 7,
        "name": "% Giá Max-Min"
    },
    "percent_max_current": {
        "index": 8,
        "name": "% Giá hiện tại\nso với giá max"
    },
    "min_time_week": {
        "index": 9,
        "name": "Min Time"
    },
    "max_time_week": {
        "index": 10,
        "name": "Max Time"
    },
    "percent_cut_loss": {
        "index": 11,
        "name": "% Cắt lỗ"
    },
    "percent_sell": {
        "index": 12,
        "name": "% Bán"
    },
    "tran_value": {
        "index": 13,
        "name": "Giá trần"
    },
    "san_value": {
        "index": 14,
        "name": "Giá sàn"
    },
    "open_value": {
        "index": 15,
        "name": "Giá mở cửa"
    },
    "sound_enable": {
        "index": 16,
        "name": "Sound"
    },
    "changT8": {
        "index": 17,
        "name": "Thay đổi\ntrong tuần"
    }
}
