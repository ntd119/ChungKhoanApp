import datetime as dt
import pytz
import time
from stock import Stock

VN_UTC = pytz.timezone('Asia/Ho_Chi_Minh')
DAY_LIST = [2, 3, 4, 5, 6]

stock = Stock()
delete_file_flag = True
while True:
    now_time = dt.datetime.now(VN_UTC)
    day_of_week = now_time.weekday() + 2
    day_of_week = 4 # delete this
    hour = now_time.hour
    if day_of_week in DAY_LIST and (9 <= hour <= 24): # <= 15
        if day_of_week == 2 and delete_file_flag:
            stock.delete_file()
            delete_file_flag = False
        if day_of_week != 2:
            delete_file_flag = True
        print(f"RUNNING...{now_time}")
        stock.update_data(day_of_week)
    time.sleep(5)
