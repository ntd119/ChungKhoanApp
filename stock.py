import pandas
from tkinter import *
import requests
import winsound
from datetime import datetime
import time

FILE_NAME = "stock-code.csv"
DELAY_TIME = 5000
END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2?sectorID=0&catID=0&capitalID=0&languageID=1"
error = ""
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
FONT_HEADER = ("Arial", 10, "bold")


class Stock:

    def __init__(self, root):
        self.stock_code_csv = []
        self.read_file()
        self.error = ""
        self.stock_data_api = []
        self.is_running = False
        self.root = root
        self.item_list = {}
        self.start_button = ()
        self.stop_button = ()
        self.status_label = ()

    def read_file(self):
        data = pandas.read_csv(f"./file/{FILE_NAME}")
        for (index, row) in data.iterrows():
            self.stock_code_csv.append({"index": index, "code": row["code"], "max": row["max"], "min": row["min"]})

    def call_api(self):
        response = requests.get(url=END_POINT, headers=HEADERS)
        if response.status_code != 200:
            self.error = "Lỗi call API"
        else:
            self.stock_data_api = response.json()
            for item_dict in self.stock_code_csv:
                stock_code = item_dict.get("code")
                stock_single = [row for row in self.stock_data_api if row["_sc_"] == stock_code.upper()]
                if len(stock_single) == 1:
                    stock_single = stock_single[0]
                    current_value = float(stock_single['_cp_'])
                    self.item_list.get(f"current_value_label_{stock_code.lower()}").config(
                        text="{:,.0f}".format(current_value))
                    radio_button_value = int(self.item_list.get(f"radio_button_value_{stock_code.lower()}").get())
                    status_label = self.item_list[f'status_label_{stock_code.lower()}']
                    if radio_button_value == 1:
                        # max
                        max_value = float(self.item_list.get(f"max_value_entry_{stock_code.lower()}").get())
                        if current_value >= max_value:
                            self.play_sound()
                            status_label.config(text="✔", foreground="green")
                        else:
                            status_label.config(text="No", foreground="black")
                    else:
                        # min
                        min_value = float(self.item_list.get(f"min_value_entry_{stock_code.lower()}").get())
                        if float(current_value) <+ float(min_value):
                            self.play_sound()
                            status_label.config(text="✔", foreground="green")
                        else:
                            status_label.config(text="No", foreground="black")
                else:
                    self.item_list.get(f"current_value_label_{stock_code.lower()}").config(text="Wrong code",
                                                                                           foreground="red")
            self.disable_button()
            if self.is_running:
                self.root.after(DELAY_TIME, self.call_api)
        now = datetime.now().time()
        format_time = now.strftime("%H:%M:%S")
        print(f"RUNNING... {format_time}")

    def start_progress(self):
        self.is_running = True
        self.call_api()
        self.show_time()

    def stop_progress(self):
        self.is_running = False
        self.disable_button()

    def draw_header(self):
        start_button = Button(text="Start", foreground="green", font=FONT_HEADER, command=self.start_progress)
        start_button.grid(column=0, row=0)
        self.start_button = start_button

        stop_button = Button(text="Stop", foreground="orange", font=FONT_HEADER, command=self.stop_progress)
        stop_button.grid(column=1, row=0)
        stop_button.config(state=DISABLED)
        self.stop_button = stop_button

        status_label = Label(text="STOPPED", foreground="red", font=FONT_HEADER)
        status_label.grid(column=2, row=0)
        self.status_label = status_label

        stock_code = Label(text="Mã ck", font=FONT_HEADER)
        stock_code.grid(column=1, row=1)

        max_value = Label(text="Max", font=FONT_HEADER)
        max_value.grid(column=2, row=1)

        current_value_label = Label(text="Giá trị hiện tại", font=FONT_HEADER)
        current_value_label.grid(column=3, row=1)

        min_value = Label(text="Min", font=FONT_HEADER)
        min_value.grid(column=4, row=1)

        radio_choose = Label(text="Selected", font=FONT_HEADER)
        radio_choose.grid(column=5, row=1)

        radio_choose = Label(text="Status", font=FONT_HEADER)
        radio_choose.grid(column=7, row=1)

    def draw_body(self):
        for item_dict in self.stock_code_csv:
            row = int(item_dict.get("index")) + 2
            checkbox_selected = IntVar()
            checkbox_selected.set(1)
            checkbox = Checkbutton(self.root, variable=checkbox_selected, textvariable=1, onvalue=1, offvalue=0)
            checkbox.grid(column=0, row=row)

            stock_code = item_dict.get("code")
            stock_code_label = Label(text=stock_code, anchor='w')
            stock_code_label.grid(column=1, row=row)

            max_value_entry = Entry()
            max_value_entry.insert(END, item_dict.get("max"))
            max_value_entry.grid(column=2, row=row)
            self.item_list[f'max_value_entry_{stock_code.lower()}'] = max_value_entry

            current_value_label = Label(text="{:,.0f}".format(0.00))
            current_value_label.grid(column=3, row=row)
            self.item_list[f'current_value_label_{stock_code.lower()}'] = current_value_label

            min_value_entry = Entry()
            min_value_entry.insert(END, item_dict.get("min"))
            min_value_entry.grid(column=4, row=row)
            self.item_list[f'min_value_entry_{stock_code.lower()}'] = min_value_entry

            radio_button_value = StringVar()
            # initialize
            radio_button_value.set(1)
            radio_1 = Radiobutton(variable=radio_button_value, value=1, text="Max")
            radio_1.grid(column=5, row=row)
            radio_2 = Radiobutton(variable=radio_button_value, value=2, text="Min")
            radio_2.grid(column=6, row=row)
            self.item_list[f'radio_button_value_{stock_code.lower()}'] = radio_button_value

            status_label = Label(text="No")
            status_label.grid(column=7, row=row)
            self.item_list[f'status_label_{stock_code.lower()}'] = status_label

    def play_sound(self):
        duration = 1000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)

    def disable_button(self):
        if self.is_running:
            self.start_button.config(state=DISABLED)
            self.stop_button.config(state=NORMAL)
        else:
            self.start_button.config(state=NORMAL)
            self.stop_button.config(state=DISABLED)
            self.status_label.config(text="STOPPED", foreground="red")

    def show_time(self):
        if self.is_running:
            now = datetime.now().time()
            format_time = now.strftime("%H:%M:%S")
            self.status_label.config(text=f"RUNNING... {format_time}", foreground="green")
            self.root.after(1000, self.show_time)
