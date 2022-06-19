import datetime
import time
import shutil


import requests
import json
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
        self.up = True
        self.data_list = None

    def connectAPI(self):
        try:
            response = requests.get(END_POINT, params=paramters, headers=HEADERS)
            self.data_list = response.json()
        except:
            time.sleep(5)
            self.connectAPI()

    def update_data(self, day_of_week: int, now_time: datetime.datetime):
        self.connectAPI()
        data_list = self.data_list
        hour = now_time.hour
        minute = now_time.minute
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
                current_time = now_time.timestamp() * 1000
                try:
                    max_price = max(data_from_file[stock_code]["max_price"], current_price)
                    min_price = min(data_from_file[stock_code]["min_price"], current_price)
                    max_price_time = data_from_file[stock_code]["max_price_time"]
                    if current_price > int(data_from_file[stock_code]["max_price"]):
                        max_price_time = current_time
                    min_price_time = data_from_file[stock_code]["min_price_time"]
                    if current_price < int(data_from_file[stock_code]["min_price"]):
                        min_price_time = current_time
                    line_price_2 = data_from_file[stock_code][f"line_price_2"]
                    line_price_3 = data_from_file[stock_code][f"line_price_3"]
                    line_price_4 = data_from_file[stock_code][f"line_price_4"]
                    line_price_5 = data_from_file[stock_code][f"line_price_5"]
                    line_price_6 = data_from_file[stock_code][f"line_price_6"]
                    if day_of_week == 2:
                        line_price_2 = self.update_line_price(line_price_2, current_price, current_time)
                    elif day_of_week == 3:
                        line_price_3 = self.update_line_price(line_price_3, current_price, current_time)
                    elif day_of_week == 4:
                        line_price_4 = self.update_line_price(line_price_4, current_price, current_time)
                    elif day_of_week == 5:
                        line_price_5 = self.update_line_price(line_price_5, current_price, current_time)
                    elif day_of_week == 6:
                        line_price_6 = self.update_line_price(line_price_6, current_price, current_time)

                except KeyError:
                    max_price = current_price
                    min_price = current_price
                    max_price_time = current_time
                    min_price_time = current_time
                    line_price_2 = []
                    line_price_3 = []
                    line_price_4 = []
                    line_price_5 = []
                    line_price_6 = []
                    if day_of_week == 2:
                        line_price_2 = self.update_line_price(line_price_2, current_price, current_time)
                    elif day_of_week == 3:
                        line_price_3 = self.update_line_price(line_price_3, current_price, current_time)
                    elif day_of_week == 4:
                        line_price_4 = self.update_line_price(line_price_4, current_price, current_time)
                    elif day_of_week == 5:
                        line_price_5 = self.update_line_price(line_price_5, current_price, current_time)
                    elif day_of_week == 6:
                        line_price_6 = self.update_line_price(line_price_6, current_price, current_time)
                try:
                    head_price = data_from_file[stock_code]["head_price"]
                    tail_price = data_from_file[stock_code]["tail_price"]
                except KeyError:
                    head_price = 0
                    tail_price = 0

                try:
                    head_price_date = data_from_file[stock_code]["head_price_date"]
                except KeyError:
                    head_price_date = ""

                if day_of_week == 2 and hour == 9 and minute == 15:
                    head_price = current_price
                    head_price_date = now_time.strftime("%d-%m-%Y")
                if day_of_week == 6 and hour == 14 and minute == 45:
                    tail_price = current_price
                stock = {
                    data["_sc_"]: {
                        "max_price": int(max_price),
                        "max_price_time": max_price_time,
                        "min_price": int(min_price),
                        "min_price_time": min_price_time,
                        "head_price": head_price,
                        "head_price_date": head_price_date,
                        "tail_price": tail_price,
                        "type": data["_in_"],
                        "line_price_2": line_price_2,
                        "line_price_3": line_price_3,
                        "line_price_4": line_price_4,
                        "line_price_5": line_price_5,
                        "line_price_6": line_price_6
                    }
                }
                data_from_file.update(stock)
            json.dump(data_from_file, stock_file, indent=4)

    def delete_file(self):
        for i in range(299, -1, -1):
            name1 = f'data/stock_T{i}.json'
            name2 = f'data/stock_T{i + 1}.json'
            if os.path.exists(name1) and os.path.exists(name2):
                shutil.copyfile(name1, name2)

    def update_line_price(self, line_price, current_price, current_time):
        if len(line_price) < 2:
            line_price = [{"price": current_price, "time": current_time},
                          {"price": current_price, "time": current_time}]
        last_item = line_price[-1]
        last_item_price = last_item["price"]
        try:
            percent_one = ((current_price - last_item_price) / last_item_price) * 100
        except ZeroDivisionError:
            percent_one = 0
        if abs(percent_one) > 1 or last_item_price == 0:
            if last_item_price <= current_price:
                if self.up:
                    line_price[-1] = ({"price": current_price, "time": current_time})
                else:
                    line_price.append({"price": current_price, "time": current_time})
                self.up = True
            else:
                if not self.up:
                    line_price[-1] = ({"price": current_price, "time": current_time})
                else:
                    line_price.append({"price": current_price, "time": current_time})
                self.up = False
        return line_price

    def check_running(self, now_time: datetime.datetime):
        with open("data/check.json", 'w') as check_file:
            data = {
                "current_time": now_time.timestamp() * 1000
            }
            json.dump(data, check_file, indent=4)
