import datetime

import requests
import json
import time
import os

HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2"
FILE_NAME = "data/stock_T0.json"
paramters = {
    "sectorID": 0,
    "catID": 0,
    "capitalID": 0,
    "languageID": 1
}


class Stock:

    def __init__(self):
        pass

    def update_data(self, day_of_week: int):
        response = requests.get(END_POINT, params=paramters, headers=HEADERS)
        response.raise_for_status()
        data_list = response.json()
        try:
            with open(FILE_NAME) as stock_file:
                data_from_file = json.load(stock_file)
        except FileNotFoundError:
            with open(FILE_NAME, "a") as stock_file:
                data_from_file = {}

        with open(FILE_NAME, 'w') as stock_file:
            for data in data_list:
                stock_code = data["_sc_"]
                current_price = int(data["_cp_"])
                current_time = round(time.time() * 1000)
                line_price: list
                try:
                    max_price = max(data_from_file[stock_code]["max_price"], current_price)
                    min_price = min(data_from_file[stock_code]["min_price"], current_price)
                    max_price_time = data_from_file[stock_code]["max_price_time"]
                    if current_price > max_price:
                        max_price_time = current_time
                    min_price_time = data_from_file[stock_code]["min_price_time"]
                    if current_price < min_price:
                        min_price_time = current_time
                    line_price = data_from_file[stock_code][f"line_price_{day_of_week}"]
                    last_item = line_price[-1]
                    last_item_price = last_item["price"]
                    if last_item_price != current_price:
                        line_price.append({"price": current_price, "time": current_time})
                except KeyError:
                    max_price = current_price
                    min_price = current_price
                    max_price_time = current_time
                    min_price_time = current_time
                    line_price = [{"price": current_price, "time": current_time},
                                  {"price": current_price, "time": current_time}]
                stock = {
                    data["_sc_"]: {
                        "max_price": int(max_price),
                        "max_price_time": max_price_time,
                        "min_price": int(min_price),
                        "min_price_time": min_price_time,
                        "type": data["_in_"],
                        f"line_price_{day_of_week}": line_price,
                    }
                }
                data_from_file.update(stock)
            json.dump(data_from_file, stock_file, indent=4)

    def delete_file(self):
        name = "data/stock_T8.json"
        if os.path.exists(name):
            os.remove(name)
        for i in range(7, -1, -1):
            os.rename(f'data/stock_T{i}.json', f'data/stock_T{i + 1}.json')
