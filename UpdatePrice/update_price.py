import requests
import json
import time
import datetime as dt

HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2"
FILE_NAME = "data/stock-code.json"
paramters = {
    "sectorID": 0,
    "catID": 0,
    "capitalID": 0,
    "languageID": 1
}

STOCK_LIST = ["ACB", "BID", "CTG", "EIB", "HDB", "LPB", "MBB", "MSB", "OCB", "SHB", "SSB", "STB", "TCB", "TPB", "VCB",
              "VIB", "VPB"]


def update_data():
    response = requests.get(END_POINT, params=paramters, headers=HEADERS)
    response.raise_for_status()
    data_list = response.json()
    print(data_list)
    try:
        with open(FILE_NAME) as stock_file:
            data_from_file = json.load(stock_file)
    except FileNotFoundError:
        with open(FILE_NAME, "a") as stock_file:
            data_from_file = {}

    with open(FILE_NAME, 'w') as stock_file:
        for data in data_list:
            stock_code = data["_sc_"]
            if stock_code in STOCK_LIST:
                current_price = data["_cp_"]
                should_buy = data_from_file[stock_code]["should_buy"]
                enable_sound = data_from_file[stock_code]["enable_sound"]
                bought = data_from_file[stock_code]["bought"]
                percent_cut_loss = data_from_file[stock_code]["percent_cut_loss"]
                percent_sell = data_from_file[stock_code]["percent_sell"]
                min_last_week = data_from_file[stock_code]["min_last_week"]
                stock = {
                    data["_sc_"]: {
                        "should_buy": should_buy,
                        "enable_sound": enable_sound,
                        "bought": bought,
                        "percent_cut_loss": percent_cut_loss,
                        "percent_sell": percent_sell,
                        "min_last_week": min_last_week,
                        "best_value": current_price
                    }
                }
                data_from_file.update(stock)
        json.dump(data_from_file, stock_file, indent=4)


while True:
    print(f"RUNNING...{dt.datetime.now()}")
    update_data()
    time.sleep(5)
