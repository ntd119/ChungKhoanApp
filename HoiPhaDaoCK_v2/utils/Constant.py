VIETSTOCK_END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2"
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
BACKGROUND_LO = "#F33232"
BACKGROUND_LAI = "#00E11A"

COLUMN_NAME = {
    "status": {
        "index": 0,
        "name": "Status"
    },
    "bought": {
        "index": 1,
        "name": "Giá mua"
    },
    "current_value": {
        "index": 2,
        "name": "Giá HT"
    },
    "lai_lo": {
        "index": 3,
        "name": "Lãi/Lỗ"
    },
    "percent_max_current": {
        "index": 4,
        "name": "% Max-HT"
    },
    "min_value_week": {
        "index": 5,
        "name": "Min week"
    },
    "min_time_week": {
        "index": 6,
        "name": "Min Time"
    },
    "max_value_week": {
        "index": 7,
        "name": "Max week"
    },
    "max_time_week": {
        "index": 8,
        "name": "Max Time"
    },
    "percent_max_min": {
        "index": 9,
        "name": "% Max-Min"
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
        "name": "Trần"
    },
    "san_value": {
        "index": 13,
        "name": "Sàn"
    },
    "open_value": {
        "index": 14,
        "name": "Mở cửa"
    },
    "sound_enable": {
        "index": 15,
        "name": "Sound"
    }
}

