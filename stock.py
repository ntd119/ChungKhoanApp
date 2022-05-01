import pandas
from tkinter import *

class Stock:

    def __init__(self):
        self.stock_code_list = []
        self.read_file()

    def read_file(self):
        data = pandas.read_csv("./file/stock-code.csv")
        for (index, row) in data.iterrows():
            self.stock_code_list.append({"index": index, "code": row["code"], "min": row["min"], "max": row["max"]})

    def draw_header(self):
        checkbox = Checkbutton()
        checkbox.grid(column=0, row=0)

        stock_code = Label(text="Mã ck")
        stock_code.grid(column=1, row=0)

        current_value = Label(text="Giá trị hiện tại")
        current_value.grid(column=2, row=0)

        min_value = Label(text="Ngưỡng min")
        min_value.grid(column=3, row=0)

        max_value = Label(text="Ngưỡng max")
        max_value.grid(column=4, row=0)

        radio_choose = Label(text="Selected")
        radio_choose.grid(column=5, row=0)