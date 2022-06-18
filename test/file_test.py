import datetime
import time
import os.path
import requests
import json
import unidecode

FIREANT_URL = "https://restv2.fireant.vn/"
FIREANT_AUTH = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxODg5NjIyNTMwLCJuYmYiOjE1ODk2MjI1MzAsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsiYWNhZGVteS1yZWFkIiwiYWNhZGVteS13cml0ZSIsImFjY291bnRzLXJlYWQiLCJhY2NvdW50cy13cml0ZSIsImJsb2ctcmVhZCIsImNvbXBhbmllcy1yZWFkIiwiZmluYW5jZS1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImludmVzdG9wZWRpYS1yZWFkIiwib3JkZXJzLXJlYWQiLCJvcmRlcnMtd3JpdGUiLCJwb3N0cy1yZWFkIiwicG9zdHMtd3JpdGUiLCJzZWFyY2giLCJzeW1ib2xzLXJlYWQiLCJ1c2VyLWRhdGEtcmVhZCIsInVzZXItZGF0YS13cml0ZSIsInVzZXJzLXJlYWQiXSwianRpIjoiMjYxYTZhYWQ2MTQ5Njk1ZmJiYzcwODM5MjM0Njc1NWQifQ.dA5-HVzWv-BRfEiAd24uNBiBxASO-PAyWeWESovZm_hj4aXMAZA1-bWNZeXt88dqogo18AwpDQ-h6gefLPdZSFrG5umC1dVWaeYvUnGm62g4XS29fj6p01dhKNNqrsu5KrhnhdnKYVv9VdmbmqDfWR8wDgglk5cJFqalzq6dJWJInFQEPmUs9BW_Zs8tQDn-i5r4tYq2U8vCdqptXoM7YgPllXaPVDeccC9QNu2Xlp9WUvoROzoQXg25lFub1IYkTrM66gJ6t9fJRZToewCt495WNEOQFa_rwLCZ1QwzvL0iYkONHS_jZ0BOhBCdW9dWSawD6iF1SIQaFROvMDH1rg"


VIETSTOCK_END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2"
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           'Authorization': FIREANT_AUTH
           }


def gia_qua_khu():
    tuan = 4
    date_1 = datetime.datetime(2022, 6, 13)
    end_date = date_1 - datetime.timedelta(days=7 * tuan)
    date_format = end_date.strftime("%Y-%m-%d")

    fireant_prams = {
        "startDate": date_format,
        "endDate": date_format
    }
    file_name = f"data/stock_T{tuan}.json"
    file_exists = os.path.exists(file_name)
    if not file_exists:
        jsonString = json.dumps({})
        jsonFile = open(file_name, "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    with open(file_name, "r") as file:
        data_from_file = json.load(file)

    with open("data/tat_ca.json", "r") as file:
        data_all = json.load(file)
    tong = len(data_all)
    row_index = 0
    with open(f"data/stock_T{tuan}.json", "w") as stock_file:
        for stock_name in data_all:
            row_index += 1
            print(f"{row_index}/{tong}")
            response = requests.get(FIREANT_URL + f"symbols/{stock_name}/historical-quotes", params=fireant_prams,
                                                                headers=HEADERS)
            data = response.json()
            if len(data) > 0:
                gia_mo_cua = data[0]["priceOpen"]
                gia_final = int(gia_mo_cua) * 1000
            dic_item = {
                stock_name: {
                    "max_price": 0,
                    "max_price_time": 0,
                    "min_price": 0,
                    "min_price_time": 0,
                    "head_price": gia_final,
                    "tail_price": 0,
                    "type": "",
                    "line_price_2": [],
                    "line_price_3": [],
                    "line_price_4": [],
                    "line_price_5": [],
                    "line_price_6": []
                }
            }
            data_from_file.update(dic_item)
        json.dump(data_from_file, stock_file, indent=4)

gia_qua_khu()