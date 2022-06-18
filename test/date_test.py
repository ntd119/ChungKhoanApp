import datetime

date_1 = datetime.datetime(2022, 6, 13)

end_date = date_1 - datetime.timedelta(days=7*3)

date_format  = end_date.strftime("%Y-%m-%d")

print(date_format)