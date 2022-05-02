import pandas
from tkinter import *
import requests
import winsound
from datetime import datetime

FILE_NAME = "stock-code.csv"
DELAY_TIME = 5000
END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2?sectorID=0&catID=0&capitalID=0&languageID=1"
error = ""
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
FONT_HEADER = ("Arial", 10, "bold")

STATUS_CHECK = "No"
timer_api = None
timer_time = None

class Stock:

    def __init__(self, root):
        self.stock_code_csv = []
        self.read_file()
        self.error = ""
        self.stock_data_api = []
        self.is_running = False
        self.root = root
        self.item_list = {}
        self.start_button = None
        self.stop_button = None
        self.status_label = None
        self.start_change_input = None
        self.end_change_input = None
        self.percent_symbol_label = None

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
                    stock_checkbox = self.item_list.get(f"stock_checkbox_{stock_code.lower()}").get()
                    status_label = self.item_list[f'status_label_{stock_code.lower()}']
                    if stock_checkbox:
                        stock_single = stock_single[0]
                        current_value = float(stock_single['_cp_'])
                        self.item_list.get(f"current_value_label_{stock_code.lower()}").config(
                            text="{:,.0f}".format(current_value))
                        radio_button_value = int(self.item_list.get(f"radio_button_value_{stock_code.lower()}").get())
                        if radio_button_value == 1:
                            # max
                            max_value = float(self.item_list.get(f"max_value_entry_{stock_code.lower()}").get())
                            if current_value >= max_value:
                                self.play_sound()
                                status_label.config(text="✔", foreground="green")
                            else:
                                status_label.config(text=STATUS_CHECK, foreground="black")
                        else:
                            # min
                            min_value = float(self.item_list.get(f"min_value_entry_{stock_code.lower()}").get())
                            if float(current_value) <+ float(min_value):
                                self.play_sound()
                                status_label.config(text="✔", foreground="green")
                            else:
                                status_label.config(text=STATUS_CHECK, foreground="black")
                    else:
                        status_label.config(text=STATUS_CHECK, foreground="black")
                else:
                    self.item_list.get(f"current_value_label_{stock_code.lower()}").config(text="Wrong code",
                                                                                           foreground="red")
            self.disable_button()
            if self.is_running:
                global timer_api
                timer_api = self.root.after(DELAY_TIME, self.call_api)
        now = datetime.now().time()
        format_time = now.strftime("%H:%M:%S")
        print(f"RUNNING... {format_time}")

    def start_progress(self):
        self.is_running = True
        self.call_api()
        self.show_time()

    def stop_progress(self):
        self.is_running = False
        self.root.after_cancel(timer_api)
        self.root.after_cancel(timer_time)
        self.disable_button()

    def draw_header(self):
        percent_change_label = Label(text="Tính % thay đổi",font=FONT_HEADER)
        percent_change_label.grid(column=0, row=0, columnspan=2)

        start_change_input = Entry()
        start_change_input.grid(column=2, row=0, columnspan=2)
        self.start_change_input = start_change_input

        to_change_label = Label(text="-",font=FONT_HEADER)
        to_change_label.grid(column=4, row=0)

        end_change_input = Entry()
        end_change_input.grid(column=5, row=0)
        self.end_change_input = end_change_input

        equal_button = Button(text="  =  ", foreground="green", font=FONT_HEADER, command=self.calculate_percent)
        equal_button.grid(column=6, row=0, columnspan=2)

        percent_symbol_label = Label(text="%", font=FONT_HEADER)
        percent_symbol_label.grid(column=8, row=0)
        self.percent_symbol_label = percent_symbol_label

        start_button = Button(text="Start", foreground="green", font=FONT_HEADER, command=self.start_progress)
        start_button.grid(column=0, row=1)
        self.start_button = start_button

        stop_button = Button(text="Stop", foreground="orange", font=FONT_HEADER, command=self.stop_progress)
        stop_button.grid(column=1, row=1)
        stop_button.config(state=DISABLED)
        self.stop_button = stop_button

        status_label = Label(text="STOPPED", foreground="red", font=FONT_HEADER)
        status_label.grid(column=2, row=1, columnspan=2)
        self.status_label = status_label

        stock_code = Label(text="Mã ck", font=FONT_HEADER)
        stock_code.grid(column=1, row=2)

        max_value = Label(text="%", font=FONT_HEADER)
        max_value.grid(column=2, row=2)

        max_value = Label(text="Max", font=FONT_HEADER)
        max_value.grid(column=3, row=2)

        current_value_label = Label(text="Giá trị hiện tại", font=FONT_HEADER)
        current_value_label.grid(column=4, row=2)

        min_value = Label(text="Min", font=FONT_HEADER)
        min_value.grid(column=5, row=2)

        radio_choose = Label(text="Selected", font=FONT_HEADER)
        radio_choose.grid(column=6, row=2, columnspan=2)

        radio_choose = Label(text="Status", font=FONT_HEADER)
        radio_choose.grid(column=8, row=2)

    def draw_body(self):
        for item_dict in self.stock_code_csv:
            row = int(item_dict.get("index")) + 3
            stock_code = item_dict.get("code")

            check_value = IntVar()
            check_value.set(1)
            stock_checkbox = Checkbutton(self.root, variable=check_value, onvalue=1, offvalue=0)
            stock_checkbox.grid(column=0, row=row)
            self.item_list[f'stock_checkbox_{stock_code.lower()}'] = check_value

            stock_code_label = Label(text=stock_code, anchor='w')
            stock_code_label.grid(column=1, row=row)

            start_value = float(item_dict.get("min"))
            end_value = float(item_dict.get("max"))
            final_value = ((end_value - start_value) / start_value) * 100
            final_value = "{:.2f}".format(final_value)
            percent_label = Label(text=f"{final_value} %", anchor='w')
            percent_label.grid(column=2, row=row)

            max_value_entry = Entry()
            max_value_entry.insert(END, item_dict.get("max"))
            max_value_entry.grid(column=3, row=row)
            self.item_list[f'max_value_entry_{stock_code.lower()}'] = max_value_entry

            current_value_label = Label(text="{:,.0f}".format(0.00))
            current_value_label.grid(column=4, row=row)
            self.item_list[f'current_value_label_{stock_code.lower()}'] = current_value_label

            min_value_entry = Entry()
            min_value_entry.insert(END, item_dict.get("min"))
            min_value_entry.grid(column=5, row=row)
            self.item_list[f'min_value_entry_{stock_code.lower()}'] = min_value_entry

            radio_button_value = StringVar()
            # initialize
            radio_button_value.set("1")
            radio_1 = Radiobutton(variable=radio_button_value, value=1, text="Max")
            radio_1.grid(column=6, row=row)
            radio_2 = Radiobutton(variable=radio_button_value, value=2, text="Min")
            radio_2.grid(column=7, row=row)
            self.item_list[f'radio_button_value_{stock_code.lower()}'] = radio_button_value

            status_label = Label(text=STATUS_CHECK)
            status_label.grid(column=8, row=row)
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
        global timer_time
        now = datetime.now().time()
        format_time = now.strftime("%H:%M:%S")
        self.status_label.config(text=f"RUNNING... {format_time}", foreground="green")
        timer_time = self.root.after(1000, self.show_time)

    def calculate_percent(self):
        start_value = self.start_change_input.get()
        end_value = self.end_change_input.get()
        if start_value.isnumeric() and end_value.isnumeric():
            start_value = float(start_value)
            end_value = float(end_value)
            final_value = ((end_value - start_value) / start_value) * 100
            if final_value >= 0:
                final_value = "{:.2f}".format(abs(final_value))
                self.percent_symbol_label.config(text=f"⬆ {final_value}%", foreground="green")
            else:
                final_value = "{:.2f}".format(abs(final_value))
                self.percent_symbol_label.config(text=f"⬇ {final_value}%", foreground="red")
        else:
            final_value = "Invalid input"
            self.percent_symbol_label.config(text=final_value)

