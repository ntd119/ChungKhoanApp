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
    hour = now_time.hour
    minute = now_time.minute
    if day_of_week in DAY_LIST and (9 <= hour <= 15):
        if hour == 9:
            if minute >= 15:
                if day_of_week == 2 and delete_file_flag:
                    stock.delete_file()
                    delete_file_flag = False
                if day_of_week != 2:
                    delete_file_flag = True
                stock.update_data(day_of_week, now_time)
        elif hour == 14:
            if minute <= 45:
                if day_of_week == 2 and delete_file_flag:
                    stock.delete_file()
                    delete_file_flag = False
                if day_of_week != 2:
                    delete_file_flag = True
                stock.update_data(day_of_week, now_time)
        else:
            if day_of_week == 2 and delete_file_flag:
                stock.delete_file()
                delete_file_flag = False
            if day_of_week != 2:
                delete_file_flag = True
            stock.update_data(day_of_week, now_time)
    stock.check_running(now_time)
    time.sleep(5)


