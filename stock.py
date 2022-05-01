from tkinter import Entry

import pandas
from tkinter import *

FONT_HEADER = ("Arial", 10, "bold")

class Stock:

    def __init__(self):
        self.stock_code_list = []
        self.read_file()

    def read_file(self):
        data = pandas.read_csv("./file/stock-code.csv")
        for (index, row) in data.iterrows():
            self.stock_code_list.append({"index": index, "code": row["code"], "min": row["min"], "max": row["max"]})

    def draw_header(self):
        stock_code = Label(text="Mã ck", font=FONT_HEADER)
        stock_code.grid(column=1, row=0)

        current_value = Label(text="Giá trị hiện tại", font=FONT_HEADER)
        current_value.grid(column=2, row=0)

        min_value = Label(text="Ngưỡng min", font=FONT_HEADER)
        min_value.grid(column=3, row=0)

        max_value = Label(text="Ngưỡng max", font=FONT_HEADER)
        max_value.grid(column=4, row=0)

        radio_choose = Label(text="Selected", font=FONT_HEADER)
        radio_choose.grid(column=5, row=0)

    def draw_body(self):
        for item_dict in self.stock_code_list:
            row = int(item_dict.get("index")) + 1
            checkbox = Checkbutton()
            checkbox.grid(column=0, row=row)

            stock_code = Label(text=item_dict.get("code"))
            stock_code.grid(column=1, row=row)

            current_value = Label(text="")
            current_value.grid(column=2, row=row)

            min_value = Entry()
            min_value.insert(END, item_dict.get("min"))
            min_value.grid(column=3, row=row)

            max_value = Entry()
            max_value.insert(END, item_dict.get("max"))
            max_value.grid(column=4, row=row)

            # radio_choose = Label(text="Selected")
            # radio_choose.grid(column=5, row=row)

            radio_button_value = StringVar()
            # initialize
            radio_button_value.set(1)
            radio_1 = Radiobutton(variable=radio_button_value, value=1, text=">=")
            radio_1.grid(column=5, row=row)
            radio_2 = Radiobutton(variable=radio_button_value, value=2, text="<=")
            radio_2.grid(column=6, row=row)

