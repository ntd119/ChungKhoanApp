VIETSTOCK_END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2"
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
COLUMN_NAME = ["Status", "Giá mua", "Giá HT", "Lãi/Lỗ", "% Max-HT", "Min week", "Time",
               "Max week", "Time", "% Max-Min",
               "% Cắt lỗ", "% Bán", "Trần", "Sàn", "Sound"]

CONSTANT_BOUGHT = 1
CONSTANT_PERCENT_CAT_LO = 10