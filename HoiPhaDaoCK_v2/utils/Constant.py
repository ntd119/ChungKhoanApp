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
FILE_VN100 = "vn100.json"
FILE_NGAN_HANG = "ngan_hang.json"
FILE_NANG_LUONG = "nang_luong.json"

COLUMN_NAME = {
    "status": {
        "index": 0,
        "name": "Status"
    },
    "bought": {
        "index": 1,
        "name": "Giá mua"
    },
    "lai_lo": {
        "index": 2,
        "name": "Lãi/Lỗ"
    },
    "current_value": {
        "index": 3,
        "name": "Giá hiện tại"
    },
    "min_value_week": {
        "index": 4,
        "name": "Giá min \ntrong tuần"
    },
    "max_value_week": {
        "index": 5,
        "name": "Giá max \ntrong tuần"
    },
    "percent_max_min": {
        "index": 6,
        "name": "% Giá Max-Min"
    },
    "percent_max_current": {
        "index": 7,
        "name": "% Giá hiện tại\nso với giá max"
    },
    "min_time_week": {
        "index": 8,
        "name": "Min Time"
    },
    "max_time_week": {
        "index": 9,
        "name": "Max Time"
    },
    "percent_cut_loss": {
        "index": 10,
        "name": "% Cắt lỗ"
    },
    "percent_sell": {
        "index": 11,
        "name": "% Bán"
    },
    "tran_value": {
        "index": 12,
        "name": "Giá trần"
    },
    "san_value": {
        "index": 13,
        "name": "Giá sàn"
    },
    "open_value": {
        "index": 14,
        "name": "Giá mở cửa"
    },
    "sound_enable": {
        "index": 15,
        "name": "Sound"
    }
}

