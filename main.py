import requests
END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2?sectorID=0&catID=0&capitalID=0&languageID=1"
error = ""
headers = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
response = requests.get(url=END_POINT, headers=headers)
if response.status_code != 200:
    error = "Error"

json_data = response.json()
filter_list = [row for row in json_data if row["_sc_"] =="VCB"]
if len(filter_list) == 1:
    dict_data = filter_list[0]
else:
    error = "Lỗi dữ liệu có nhiều hơn 1 dòng"

print(dict_data)
