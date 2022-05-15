import pandas
from tkinter import *
import requests
import winsound
from datetime import datetime, time
import tkinter.messagebox
import json

FILE_NAME = "./file/stock-code.json"
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
COLOR_ERROR = "#F7DC6F"
COLOR_OK = "white"

ENTRY_WIDTH = 10


class Stock:

    def __init__(self, root):
        self.stock_code_from_file = []
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
        self.stock_code_input_header = None
        self.check_all_checkbox = None
        self.all_max_min_value = None
        self.check_delete_checkbox = None
        self.khoang_cach_an_toan_min_input = None
        self.khoang_cach_an_toan_max_input = None
        self.khoang_cach_an_toan_cal_button = None
        self.khoang_cach_an_toan_result_min_input = None
        self.khoang_cach_an_toan_result_max_input = None
        self.khoang_cach_an_toan_to_input = None

    def read_file(self):
        with open(FILE_NAME) as data_file:
            data = json.load(data_file)
            self.stock_code_from_file = data

    def call_api(self):
        try:
            response = requests.get(url=END_POINT, headers=HEADERS)
        except ConnectionError as error:
            self.error = error
            print(self.error)
            self.call_api()
        else:
            if response.status_code != 200:
                self.error = "Lỗi call API"
                print(self.error)
                self.call_api()
            else:
                self.stock_data_api = response.json()
                for stock_code in self.stock_code_from_file:
                    item_dict = self.stock_code_from_file[stock_code]
                    stock_single = [row for row in self.stock_data_api if row["_sc_"] == stock_code.upper()]
                    if len(stock_single) == 1:
                        stock_checkbox = self.item_list.get(f"stock_checkbox_{stock_code.lower()}").get()
                        status_label = self.item_list[f'status_label_{stock_code.lower()}']
                        # if stock_checkbox:
                        stock_single = stock_single[0]
                        # giá trần _clp_
                        gia_tran = float(stock_single['_clp_'])
                        self.item_list.get(f"gia_tran_label_{stock_code.lower()}").config(
                            text="{:,.0f}".format(gia_tran))
                        # giá sàn _fp_
                        gia_san = float(stock_single['_fp_'])
                        self.item_list.get(f"gia_san_label_{stock_code.lower()}").config(
                            text="{:,.0f}".format(gia_san))
                        # giá mở cửa _op_
                        gia_mo_cua = float(stock_single['_op_'])
                        self.item_list.get(f"gia_mo_cua_label_{stock_code.lower()}").config(
                            text="{:,.0f}".format(gia_mo_cua))
                        # giá hiện tại
                        current_value = float(stock_single['_cp_'])
                        percent = stock_single['_pc_']
                        final_value = "{:.2f}".format(percent)
                        if percent < 0:
                            self.item_list.get(f"current_value_label_{stock_code.lower()}").config(
                                text="{:,.0f}".format(current_value) + " (" + final_value + "%)", bg="#F33232")
                        else:
                            self.item_list.get(f"current_value_label_{stock_code.lower()}").config(
                                text="{:,.0f}".format(current_value) + " (" + final_value + "%)", bg="#00E11A")
                        radio_button_value = int(
                            self.item_list.get(f"radio_button_value_{stock_code.lower()}").get())
                        if radio_button_value == 1:
                            # max
                            max_value = float(self.item_list.get(f"max_value_entry_{stock_code.lower()}").get())
                            if current_value >= max_value:
                                status_label.config(text="Bán", foreground="green")
                                if stock_checkbox:
                                    self.play_sound()
                            else:
                                status_label.config(text=STATUS_CHECK, foreground="black")
                        else:
                            # min
                            min_value = float(self.item_list.get(f"min_value_entry_{stock_code.lower()}").get())
                            if float(current_value) <= float(min_value):
                                status_label.config(text="Mua", foreground="green")
                                if stock_checkbox:
                                    self.play_sound()
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
        percent_change_label = Label(text="Tính % thay đổi", font=FONT_HEADER)
        percent_change_label.grid(column=0, row=0, columnspan=2)

        start_change_input = Entry()
        start_change_input.grid(column=2, row=0, columnspan=2)
        self.start_change_input = start_change_input

        to_change_label = Label(text="-", font=FONT_HEADER)
        to_change_label.grid(column=4, row=0)

        end_change_input = Entry()
        end_change_input.grid(column=5, row=0)
        self.end_change_input = end_change_input

        equal_button = Button(text="  =  ", foreground="green", font=FONT_HEADER, command=self.calculate_percent)
        equal_button.grid(column=6, row=0, columnspan=1)

        percent_symbol_label = Label(text="%", font=FONT_HEADER)
        percent_symbol_label.grid(column=7, row=0)
        self.percent_symbol_label = percent_symbol_label

        stock_code_label_header = Label(text="Mã CK:", font=FONT_HEADER)
        stock_code_label_header.grid(column=8, row=0)

        stock_code_input_header = Entry(width=7)
        stock_code_input_header.grid(column=9, row=0)
        self.stock_code_input_header = stock_code_input_header

        add_to_file_button_header = Button(text="Add", foreground="green", font=FONT_HEADER,
                                           command=self.add_stock_to_file)
        add_to_file_button_header.grid(column=10, row=0)

        # Khoang cach an toàn
        khoang_cach_an_toan_row = 1
        khoang_cach_an_toan_label = Label(text="Khoảng cách an toàn:", font=FONT_HEADER)
        khoang_cach_an_toan_label.grid(column=0, row=khoang_cach_an_toan_row, columnspan=2)

        khoang_cach_an_toan_min_input = Entry()
        khoang_cach_an_toan_min_input.grid(column=2, row=khoang_cach_an_toan_row, columnspan=2)
        self.khoang_cach_an_toan_min_input = khoang_cach_an_toan_min_input

        khoang_cach_an_toan_to_input = Entry(width=4)
        khoang_cach_an_toan_to_input.insert(END, 4)
        khoang_cach_an_toan_to_input.grid(column=4, row=khoang_cach_an_toan_row)
        self.khoang_cach_an_toan_to_input = khoang_cach_an_toan_to_input

        khoang_cach_an_toan_max_input = Entry()
        khoang_cach_an_toan_max_input.grid(column=5, row=khoang_cach_an_toan_row)
        self.khoang_cach_an_toan_max_input = khoang_cach_an_toan_max_input

        khoang_cach_an_toan_cal_button = Button(text="  =  ", foreground="green", font=FONT_HEADER, command=self.distance_value)
        khoang_cach_an_toan_cal_button.grid(column=6, row=khoang_cach_an_toan_row, columnspan=1)
        self.khoang_cach_an_toan_cal_button = khoang_cach_an_toan_cal_button

        khoang_cach_an_toan_result_min_input = Entry()
        khoang_cach_an_toan_result_min_input.grid(column=7, row=khoang_cach_an_toan_row, columnspan=2)
        self.khoang_cach_an_toan_result_min_input = khoang_cach_an_toan_result_min_input

        khoang_cach_an_toan_result_max_input = Entry()
        khoang_cach_an_toan_result_max_input.grid(column=9, row=khoang_cach_an_toan_row, columnspan=2)
        self.khoang_cach_an_toan_result_max_input = khoang_cach_an_toan_result_max_input

        start_button = Button(text="Start", foreground="green", font=FONT_HEADER, command=self.start_progress)
        start_button.grid(column=0, row=2)
        self.start_button = start_button

        stop_button = Button(text="Stop", foreground="orange", font=FONT_HEADER, command=self.stop_progress)
        stop_button.grid(column=1, row=2)
        stop_button.config(state=DISABLED)
        self.stop_button = stop_button

        save_all_button = Button(text="Save", foreground="green", font=FONT_HEADER, command=self.save_all)
        save_all_button.grid(column=2, row=2)

        status_label = Label(text="STOPPED", foreground="red", font=FONT_HEADER)
        status_label.grid(column=3, row=2, columnspan=2)
        self.status_label = status_label

        column_body = 0

        delete_button = Button(text="Delete", command=self.delete_record, foreground="red", font=FONT_HEADER)
        delete_button.grid(column=column_body, row=3)

        check_delete = IntVar()
        check_delete.set(0)
        delete_all_checkbox = Checkbutton(self.root, text="Del", variable=check_delete, onvalue=1, offvalue=0,
                                          font=FONT_HEADER, command=self.check_delete_record)
        column_body += 1
        delete_all_checkbox.grid(column=column_body, row=3)
        self.check_delete_checkbox = check_delete

        check_value = IntVar()
        check_value.set(0)
        check_all_checkbox = Checkbutton(self.root, text="Sound", variable=check_value, onvalue=1, offvalue=0,
                                         font=FONT_HEADER, command=self.check_all_function)
        column_body += 1
        check_all_checkbox.grid(column=column_body, row=3)
        self.check_all_checkbox = check_value

        stock_code = Label(text="Mã ck", font=FONT_HEADER)
        column_body += 1
        stock_code.grid(column=column_body, row=3)

        max_value = Label(text="%", font=FONT_HEADER)
        column_body += 1
        max_value.grid(column=column_body, row=3)

        max_value = Label(text="Bán", font=FONT_HEADER)
        column_body += 1
        max_value.grid(column=column_body, row=3)

        gia_tran_label = Label(text="Trần", font=FONT_HEADER)
        column_body += 1
        gia_tran_label.grid(column=column_body, row=3)

        gia_san_label = Label(text="Sàn", font=FONT_HEADER)
        column_body += 1
        gia_san_label.grid(column=column_body, row=3)

        gia_mo_cua_label = Label(text="Mở cửa", font=FONT_HEADER)
        column_body += 1
        gia_mo_cua_label.grid(column=column_body, row=3)

        current_value_label = Label(text="Hiện tại", font=FONT_HEADER)
        column_body += 1
        current_value_label.grid(column=column_body, row=3)

        min_value = Label(text="Mua", font=FONT_HEADER)
        column_body += 1
        min_value.grid(column=column_body, row=3)

        gia_da_mua_label = Label(text="Đã mua", font=FONT_HEADER)
        column_body += 1
        gia_da_mua_label.grid(column=column_body, row=3)

        lai_lo_label = Label(text="Lãi/lỗ", font=FONT_HEADER)
        column_body += 1
        lai_lo_label.grid(column=column_body, row=3)

        all_max_min_value = StringVar()
        # initialize
        all_max_min_value.set("2")
        all_max_radio = Radiobutton(variable=all_max_min_value, value=1, text="All bán", font=FONT_HEADER,
                                    command=self.all_max_min_function)
        column_body += 1
        all_max_radio.grid(column=column_body, row=3)

        all_min_radio = Radiobutton(variable=all_max_min_value, value=2, text="All mua", font=FONT_HEADER,
                                    command=self.all_max_min_function)
        column_body += 1
        all_min_radio.grid(column=column_body, row=3)
        self.all_max_min_value = all_max_min_value

        radio_choose = Label(text="Status", font=FONT_HEADER)
        column_body += 1
        radio_choose.grid(column=column_body, row=3)

    def draw_body(self):
        row = 4
        for stock_code in self.stock_code_from_file:
            item_dict = self.stock_code_from_file[stock_code]
            column_index = 1
            # delete
            check_delete = IntVar()
            check_delete.set(0)
            delete_checkbox = Checkbutton(self.root, variable=check_delete, onvalue=1, offvalue=0)
            delete_checkbox.grid(column=column_index, row=row)
            self.item_list[f'delete_checkbox_{stock_code.lower()}'] = check_delete

            check_value = IntVar()
            check_value.set(int(item_dict.get("check_enable")))
            stock_checkbox = Checkbutton(self.root, variable=check_value, onvalue=1, offvalue=0)
            column_index += 1
            stock_checkbox.grid(column=column_index, row=row, columnspan=2)
            self.item_list[f'stock_checkbox_{stock_code.lower()}'] = check_value

            stock_code_label = Label(text=stock_code, anchor='w')
            column_index += 1
            stock_code_label.grid(column=column_index, row=row)

            start_value = float(item_dict.get("min"))
            end_value = float(item_dict.get("max"))
            final_value = ((end_value - start_value) / start_value) * 100
            final_value = "{:.2f}".format(final_value)
            percent_label = Label(text=f"{final_value} %", anchor='w')
            column_index += 1
            percent_label.grid(column=column_index, row=row)

            max_value_entry = Entry(width=ENTRY_WIDTH)
            max_value_entry.insert(END, item_dict.get("max"))
            column_index += 1
            max_value_entry.grid(column=column_index, row=row)
            self.item_list[f'max_value_entry_{stock_code.lower()}'] = max_value_entry

            gia_tran_label = Label(text="{:,.0f}".format(0.00))
            column_index += 1
            gia_tran_label.grid(column=column_index, row=row)
            self.item_list[f'gia_tran_label_{stock_code.lower()}'] = gia_tran_label

            gia_san_label = Label(text="{:,.0f}".format(0.00))
            column_index += 1
            gia_san_label.grid(column=column_index, row=row)
            self.item_list[f'gia_san_label_{stock_code.lower()}'] = gia_san_label

            gia_mo_cua_label = Label(text="{:,.0f}".format(0.00))
            column_index += 1
            gia_mo_cua_label.grid(column=column_index, row=row)
            self.item_list[f'gia_mo_cua_label_{stock_code.lower()}'] = gia_mo_cua_label

            current_value_label = Label(text="{:,.0f}".format(0.00))
            column_index += 1
            current_value_label.grid(column=column_index, row=row)
            self.item_list[f'current_value_label_{stock_code.lower()}'] = current_value_label

            min_value_entry = Entry(width=ENTRY_WIDTH)
            min_value_entry.insert(END, item_dict.get("min"))
            column_index += 1
            min_value_entry.grid(column=column_index, row=row)
            self.item_list[f'min_value_entry_{stock_code.lower()}'] = min_value_entry

            gia_da_mua_entry = Entry(width=ENTRY_WIDTH)
            gia_da_mua_entry.insert(END, 0)
            column_index += 1
            gia_da_mua_entry.grid(column=column_index, row=row)
            self.item_list[f'gia_da_mua_entry_{stock_code.lower()}'] = gia_da_mua_entry

            lai_lo_label = Label(text="0")
            column_index += 1
            lai_lo_label.grid(column=column_index, row=row)

            radio_button_value = StringVar()
            # initialize
            radio_button_value.set(int(item_dict.get("max_min_radio")))
            radio_1 = Radiobutton(variable=radio_button_value, value=1, text="Bán")
            column_index += 1
            radio_1.grid(column=column_index, row=row)
            radio_2 = Radiobutton(variable=radio_button_value, value=2, text="Mua")
            column_index += 1
            radio_2.grid(column=column_index, row=row)
            self.item_list[f'radio_button_value_{stock_code.lower()}'] = radio_button_value

            status_label = Label(text=STATUS_CHECK)
            column_index += 1
            status_label.grid(column=column_index, row=row)
            self.item_list[f'status_label_{stock_code.lower()}'] = status_label
            row += 1

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
                self.percent_symbol_label.config(text=f"⬆ {final_value} %", foreground="green")
            else:
                final_value = "{:.2f}".format(abs(final_value))
                self.percent_symbol_label.config(text=f"⬇ {final_value} %", foreground="red")
        else:
            tkinter.messagebox.showerror("Error", "Invalid input")
            self.percent_symbol_label.config(text="%")

    def add_stock_to_file(self):
        start_value = self.start_change_input.get()
        end_value = self.end_change_input.get()
        stock_code = self.stock_code_input_header.get()
        if start_value.isnumeric() and end_value.isnumeric() and len(stock_code.strip()) != 0:
            with open(FILE_NAME, 'w') as data_file:
                new_data = {
                    stock_code.upper(): {
                        "max": end_value,
                        "min": start_value,
                        "check_enable": 0,
                        "max_min_radio": "2"
                    }
                }
                self.stock_code_from_file.update(new_data)
                json.dump(self.stock_code_from_file, data_file, indent=4)
                self.draw_body()
            tkinter.messagebox.showinfo("Success", "Add stock successful")
        else:
            tkinter.messagebox.showerror("Error", "Invalid input")

    def check_all_function(self):
        value = int(self.check_all_checkbox.get())
        for stock_code in self.stock_code_from_file:
            check_value = self.item_list[f'stock_checkbox_{stock_code.lower()}']
            if value == 0:
                check_value.set(0)
            else:
                check_value.set(1)

    def all_max_min_function(self):
        value = int(self.all_max_min_value.get())
        for stock_code in self.stock_code_from_file:
            radio_button = self.item_list[f'radio_button_value_{stock_code.lower()}']
            if value == 1:
                radio_button.set(1)
            else:
                radio_button.set(2)

    def save_all(self):
        with open(FILE_NAME, 'w') as data_file:
            for stock_code in self.stock_code_from_file:
                update_data = {
                    stock_code: {
                        "max": self.item_list[f'max_value_entry_{stock_code.lower()}'].get(),
                        "min": self.item_list[f'min_value_entry_{stock_code.lower()}'].get(),
                        "check_enable": self.item_list[f'stock_checkbox_{stock_code.lower()}'].get(),
                        "max_min_radio": self.item_list[f'radio_button_value_{stock_code.lower()}'].get()
                    }
                }
                self.stock_code_from_file.update(update_data)
            json.dump(self.stock_code_from_file, data_file, indent=4)
            tkinter.messagebox.showinfo("Success", "Save successful!")

    def check_delete_record(self):
        value = int(self.check_delete_checkbox.get())
        for stock_code in self.stock_code_from_file:
            check_value = self.item_list[f'delete_checkbox_{stock_code.lower()}']
            if value == 0:
                check_value.set(0)
            else:
                check_value.set(1)

    def delete_record(self):
        check_exist = False
        for stock_code in self.stock_code_from_file:
            check_value = self.item_list[f'delete_checkbox_{stock_code.lower()}']
            value = int(check_value.get())
            if value:
                check_exist = True
        if not check_exist:
            tkinter.messagebox.showinfo("Info", "No Records Selected")
        else:
            if tkinter.messagebox.askokcancel(title="Confirm Delete", message="Are you sure you want to delete selected items?"):
                delete_list = []
                for stock_code in self.stock_code_from_file:
                    check_value = self.item_list[f'delete_checkbox_{stock_code.lower()}']
                    value = int(check_value.get())
                    if value:
                        delete_list.append(stock_code)
                for item in delete_list:
                    self.stock_code_from_file.pop(item)
                with open(FILE_NAME, 'w') as data_file:
                    json.dump(self.stock_code_from_file, data_file, indent=4)
                self.read_file()
                self.draw_body()

    def distance_value(self):
        start_value = self.khoang_cach_an_toan_min_input.get()
        end_value = self.khoang_cach_an_toan_max_input.get()
        percent_input = self.khoang_cach_an_toan_to_input.get()
        if not self.isfloat(start_value):
            tkinter.messagebox.showerror("Error", "Invalid min input")
            self.khoang_cach_an_toan_min_input.config(bg=COLOR_ERROR)
            self.khoang_cach_an_toan_max_input.config(bg=COLOR_OK)
            self.khoang_cach_an_toan_to_input.config(bg=COLOR_OK)
            self.khoang_cach_an_toan_min_input.focus()
        elif not self.isfloat(end_value):
            tkinter.messagebox.showerror("Error", "Invalid max input")
            self.khoang_cach_an_toan_max_input.config(bg=COLOR_ERROR)
            self.khoang_cach_an_toan_min_input.config(bg=COLOR_OK)
            self.khoang_cach_an_toan_to_input.config(bg=COLOR_OK)
            self.khoang_cach_an_toan_max_input.focus()
        elif not self.isfloat(percent_input):
            tkinter.messagebox.showerror("Error", "Invalid percent input")
            self.khoang_cach_an_toan_to_input.config(bg=COLOR_ERROR)
            self.khoang_cach_an_toan_min_input.config(bg=COLOR_OK)
            self.khoang_cach_an_toan_max_input.config(bg=COLOR_OK)
            self.khoang_cach_an_toan_to_input.focus()
        else:
            min_input = float(start_value)
            max_input = float(end_value)
            percent = ((max_input - min_input) / min_input) * 100
            percent_input_float = float(percent_input)
            while percent > percent_input_float:
                max_input -= 1
                min_input += 1
                percent = ((max_input - min_input) / min_input) * 100
            while percent < percent_input_float:
                max_input += 1
                min_input -= 1
                percent = ((max_input - min_input) / min_input) * 100
            self.khoang_cach_an_toan_result_min_input.delete(0, END)
            self.khoang_cach_an_toan_result_min_input.insert(END, int(min_input))
            self.khoang_cach_an_toan_result_max_input.delete(0, END)
            self.khoang_cach_an_toan_result_max_input.insert(END, int(max_input))
            self.khoang_cach_an_toan_min_input.config(bg=COLOR_OK)
            self.khoang_cach_an_toan_max_input.config(bg=COLOR_OK)
            self.khoang_cach_an_toan_to_input.config(bg=COLOR_OK)

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False