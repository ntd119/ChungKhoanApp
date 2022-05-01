from tkinter import Entry

import pandas
from tkinter import *
import requests
import winsound

DELAY_TIME = 5000
END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2?sectorID=0&catID=0&capitalID=0&languageID=1"
error = ""
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
FONT_HEADER = ("Arial", 10, "bold")
class Stock:

    def __init__(self):
        self.stock_code_csv = []
        self.read_file()
        self.error = ""
        self.stock_data_api = []
        self.is_running= False

    def read_file(self):
        data = pandas.read_csv("./file/stock-code.csv")
        for (index, row) in data.iterrows():
            self.stock_code_csv.append({"index": index, "code": row["code"], "min": row["min"], "max": row["max"]})

    def call_api(self):
        response = requests.get(url=END_POINT, headers=HEADERS)
        if response.status_code != 200:
            self.error = "Lỗi call API"
        else:
            self.stock_data_api = response.json()


    def draw_header(self):
        start_button = Button(text="Start", foreground="green", font=FONT_HEADER)
        start_button.grid(column=0, row=0)
        stop_button = Button(text="Stop", foreground="orange", font=FONT_HEADER)
        stop_button.grid(column=1, row=0)

        stock_code = Label(text="Mã ck", font=FONT_HEADER)
        stock_code.grid(column=1, row=1)

        current_value_label = Label(text="Giá trị hiện tại", font=FONT_HEADER)
        current_value_label.grid(column=2, row=1)

        min_value = Label(text="Ngưỡng min", font=FONT_HEADER)
        min_value.grid(column=3, row=1)

        max_value = Label(text="Ngưỡng max", font=FONT_HEADER)
        max_value.grid(column=4, row=1)

        radio_choose = Label(text="Selected", font=FONT_HEADER)
        radio_choose.grid(column=5, row=1)

        radio_choose = Label(text="Status", font=FONT_HEADER)
        radio_choose.grid(column=7, row=1)

    def draw_body(self):
        # self.call_api()
        for item_dict in self.stock_code_csv:
            stock_code = item_dict.get("code");
            stock_single = [row for row in self.stock_data_api if row["_sc_"] == stock_code.upper()]
            if len(stock_single) != 1:
                self.error = "Mã cổ phiếu không đúng"
                current_value = 0
            else:
                stock_single = stock_single[0]
                current_value = stock_single.get('_clp_')

            row = int(item_dict.get("index")) + 2
            checkbox = Checkbutton()
            checkbox.grid(column=0, row=row)

            stock_code = Label(text=item_dict.get("code"))
            stock_code.grid(column=1, row=row)

            current_value_label = Label(text="{:,.0f}".format(current_value))
            current_value_label.grid(column=2, row=row)

            min_value_entry = Entry()
            min_value_entry.insert(END, item_dict.get("min"))
            min_value_entry.grid(column=3, row=row)

            max_value_entry = Entry()
            max_value_entry.insert(END, item_dict.get("max"))
            max_value_entry.grid(column=4, row=row)

            radio_button_value = StringVar()
            # initialize
            radio_button_value.set(1)
            radio_1 = Radiobutton(variable=radio_button_value, value=1, text="<=")
            radio_1.grid(column=5, row=row)
            radio_2 = Radiobutton(variable=radio_button_value, value=2, text=">=")
            radio_2.grid(column=6, row=row)

            status_label = Label(text="No")
            status_label.grid(column=7, row=row)

            value = int(radio_button_value.get())
            if value == 1:
                # <=
                if float(current_value) <= float(min_value_entry.get()):
                    # self.play_sound()
                    status_label.config(text="✔", foreground="red")
            else:
                # >=
                if float(current_value) >= float(max_value_entry.get()):
                    # self.play_sound()
                    status_label.config(text="✔", foreground="red")

    def play_sound(self):
        duration = 1000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)