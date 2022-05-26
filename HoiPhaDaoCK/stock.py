from tkinter import *
import requests
import winsound
from datetime import datetime
import tkinter.messagebox
import json
import plotly.graph_objects as go

FILE_NAME = "./data/stock-code.json"
DELAY_TIME = 5000
END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2?sectorID=0&catID=0&capitalID=0&languageID=1"
error = ""
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
FONT_HEADER = ("Arial", 10, "bold")

END_POINT_DATA = "https://topchonlua.com/batch/data/stock_T0.json"

STATUS_CHECK = "No"
timer_api = None
timer_time = None
COLOR_ERROR = "#F7DC6F"
COLOR_OK = "white"

ENTRY_WIDTH = 10
PERCENT_DESIRE = 4
BACKGROUND_COLOR = "#F0F0F0"
BACKGROUND_LAI = "#00E11A"

ROWS, COLS = 0, 0
ROWS_DISP = 15
COLS_DISP = 15
AM_COLOR_BACKGROUND = "#DE3163"
PM_COLOR_BACKGROUND = "#FF7F50"

STOCK_LIST = ["ACB", "BID", "CTG", "EIB", "HDB", "LPB", "MBB", "MSB", "OCB", "SHB", "SSB", "STB", "TCB", "TPB", "VCB",
              "VIB", "VPB"]


class Stock(Tk):
    def __init__(self, title='Hội Phá Đảo CK', *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.stock_code_from_file = []
        self.error = ""
        self.stock_data_api = []
        self.is_running = False
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
        self.background_color = BACKGROUND_COLOR
        self.frame = None
        self.collection_data = None

        self.get_data_from_collection()

        master_frame = Frame(self, bd=3, relief=RIDGE)
        master_frame.grid(sticky=NSEW)
        master_frame.columnconfigure(0, weight=1)

        label1 = Label(master_frame, text='MTD TEAM')
        label1.grid(row=0, column=0, pady=5, sticky=NW)

        frame2 = Frame(master_frame, bd=2, relief=FLAT)
        frame2.grid(row=3, column=0, sticky=NW)

        canvas = Canvas(frame2)
        canvas.grid(row=0, column=0)

        vsbar = Scrollbar(frame2, orient=VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=NS)
        canvas.configure(yscrollcommand=vsbar.set)

        hsbar = Scrollbar(frame2, orient=HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=EW)
        canvas.configure(xscrollcommand=hsbar.set)

        frame = Frame(canvas)
        self.frame = frame
        self.draw_table(frame)
        canvas.create_window((0, 0), window=frame, anchor=NW)

        frame.update_idletasks()
        bbox = canvas.bbox(ALL)

        w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
        dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
        canvas.configure(scrollregion=bbox, width=dw, height=dh)

    def get_data_from_collection(self):
        response = requests.get(END_POINT_DATA, headers=HEADERS)
        response.raise_for_status()
        data_list = response.json()
        self.collection_data = {key: value for (key, value) in data_list.items() if key in STOCK_LIST}

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
                flag_sound = False
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
                        status_label.config(text=STATUS_CHECK, foreground="black")
                        # Lãi/lỗ
                        self.item_list.get(f"lai_lo_label_{stock_code.lower()}").config(
                            text="0", bg=BACKGROUND_COLOR)
                        try:
                            gia_da_mua = int(self.item_list.get(f"gia_da_mua_entry_{stock_code.lower()}").get())
                        except ValueError:
                            gia_da_mua = 0
                        if gia_da_mua > 0:
                            tinh_lai = ((current_value - gia_da_mua) / gia_da_mua) * 100
                            final_tinh_lai = "{:.2f}".format(tinh_lai)
                            if tinh_lai < 0:
                                self.item_list.get(f"lai_lo_label_{stock_code.lower()}").config(
                                    text=final_tinh_lai + "%", bg="#F33232")
                                percent_cut_loss = float(
                                    self.item_list[f'percent_cut_loss_entry_{stock_code.lower()}'].get())
                                if abs(tinh_lai) > percent_cut_loss:
                                    status_label.config(text="Cắt lỗ", foreground="red")
                                    if stock_checkbox:
                                        flag_sound = True
                            else:
                                percent_sell = float(
                                    self.item_list[f'percent_sell_entry_{stock_code.lower()}'].get())
                                self.item_list.get(f"lai_lo_label_{stock_code.lower()}").config(
                                    text=final_tinh_lai + "%", bg="#00E11A")
                                if abs(tinh_lai) > percent_sell:
                                    status_label.config(text="Bán", foreground="green")
                                    if stock_checkbox:
                                        flag_sound = True
                        # else:
                        # Nên mua
                        # should_buy = float(self.item_list[f'min_value_entry_{stock_code.lower()}'].get())
                        # min_value_last_week = float(
                        #     self.item_list[f'min_value_this_week_label_{stock_code.lower()}'].get())
                        # if min_value_last_week > 0 and should_buy > 0:
                        #     gia_dao_dong = float((
                        #                                  current_value - min_value_last_week) / min_value_last_week) * 100
                        #     if gia_dao_dong > 0 and abs(gia_dao_dong) >= 1.2 and should_buy > min_value_last_week:
                        #         status_label.config(text="Nên mua", foreground="green")
                        #         if stock_checkbox:
                        #             flag_sound = True

                        # % gía tốt nhất - giá hiện tại
                        gia_tot_nhat = int(self.item_list[f'gia_tot_nhat_entry_{stock_code.lower()}'].get())
                        if gia_tot_nhat > 0:
                            percent_gia_tot_nhat = ((gia_tot_nhat - gia_da_mua) / gia_da_mua) * 100
                            percent_gia_tot_nhat = float("{:.2f}".format(percent_gia_tot_nhat))

                            percent_hien_tai = ((current_value - gia_da_mua) / gia_da_mua) * 100
                            percent_hien_tai = float("{:.2f}".format(percent_hien_tai))

                            self.percent_gia_tot_nhat_hien_tai(percent_gia_tot_nhat, percent_hien_tai, self.item_list[
                                f'percent_gia_tot_nhat_hien_tai_label_{stock_code.lower()}'])
                        else:
                            self.item_list[
                                f'percent_gia_tot_nhat_hien_tai_label_{stock_code.lower()}'].config(text="0")
                    else:
                        self.item_list.get(f"current_value_label_{stock_code.lower()}").config(text="Wrong code",
                                                                                               foreground="red")
                if flag_sound:
                    self.play_sound()

                self.disable_button()
                if self.is_running:
                    global timer_api
                    timer_api = self.after(DELAY_TIME, self.call_api)
            now = datetime.now().time()
            format_time = now.strftime("%H:%M:%S")
            print(f"RUNNING... {format_time}")

    def play_sound(self):
        duration = 1000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)

    def add_stock_to_file(self):
        start_value = self.start_change_input.get()
        end_value = self.end_change_input.get()
        stock_code = self.stock_code_input_header.get()
        if start_value.isnumeric() and end_value.isnumeric() and len(stock_code.strip()) != 0:
            with open(FILE_NAME, 'w') as data_file:
                new_data = {
                    stock_code.upper(): {
                        "should_buy": start_value,
                        "enable_sound": 0,
                        "bought": "0",
                        "percent_cut_loss": "4.0",
                        "percent_sell": "4.0",
                        "min_last_week": "0"
                    }
                }
                self.stock_code_from_file.update(new_data)
                json.dump(self.stock_code_from_file, data_file, indent=4)
                self.draw_body()
            tkinter.messagebox.showinfo("Success", "Add stock successful")
        else:
            tkinter.messagebox.showerror("Error", "Invalid input")

    def start_progress(self):
        self.is_running = True
        self.call_api()
        self.show_time()

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def stop_progress(self):
        self.is_running = False
        self.after_cancel(timer_api)
        self.after_cancel(timer_time)
        self.disable_button()

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
        timer_time = self.after(1000, self.show_time)

    def check_all_function(self):
        value = int(self.check_all_checkbox.get())
        for stock_code in self.stock_code_from_file:
            check_value = self.item_list[f'stock_checkbox_{stock_code.lower()}']
            if value == 0:
                check_value.set(0)
            else:
                check_value.set(1)

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

    def save_all(self):
        with open(FILE_NAME, 'w') as data_file:
            for stock_code in self.stock_code_from_file:
                update_data = {
                    stock_code: {
                        "should_buy": self.item_list[f'min_value_entry_{stock_code.lower()}'].get(),
                        "enable_sound": self.item_list[f'stock_checkbox_{stock_code.lower()}'].get(),
                        "bought": self.item_list[f'gia_da_mua_entry_{stock_code.lower()}'].get(),
                        "percent_cut_loss": self.item_list[f'percent_cut_loss_entry_{stock_code.lower()}'].get(),
                        "percent_sell": self.item_list[f'percent_sell_entry_{stock_code.lower()}'].get(),
                        "best_value": self.item_list[f'gia_tot_nhat_entry_{stock_code.lower()}'].get()
                    }
                }
                self.stock_code_from_file.update(update_data)
            json.dump(self.stock_code_from_file, data_file, indent=4)
            tkinter.messagebox.showinfo("Success", "Save successful!")

    def percent_lai_lo(self, start_value, end_value, label: Label):
        final_value = ((end_value - start_value) / start_value) * 100
        if final_value >= 0:
            final_value = "{:.2f}".format(abs(final_value))
            label.config(text=f"{final_value}%", bg="#00E11A")
        else:
            final_value = "{:.2f}".format(abs(final_value))
            label.config(text=f"{final_value}%", bg="#F33232")
        return final_value

    def update_gia_tot_nhat(self):
        response = requests.get(END_POINT, headers=HEADERS)
        response.raise_for_status()
        data_list = response.json()
        try:
            with open(FILE_NAME) as stock_file:
                data_from_file = json.load(stock_file)
        except FileNotFoundError:
            with open(FILE_NAME, "a") as stock_file:
                data_from_file = {}

        with open(FILE_NAME, 'w') as stock_file:
            for data in data_list:
                stock_code = data["_sc_"]
                if stock_code in STOCK_LIST:
                    current_price = int(data["_cp_"])
                    should_buy = data_from_file[stock_code]["should_buy"]
                    enable_sound = data_from_file[stock_code]["enable_sound"]
                    percent_cut_loss = data_from_file[stock_code]["percent_cut_loss"]
                    percent_sell = data_from_file[stock_code]["percent_sell"]
                    min_last_week = data_from_file[stock_code]["min_last_week"]
                    bought = data_from_file[stock_code]["bought"]
                    stock = {
                        data["_sc_"]: {
                            "should_buy": should_buy,
                            "enable_sound": enable_sound,
                            "bought": bought,
                            "percent_cut_loss": percent_cut_loss,
                            "percent_sell": percent_sell,
                            "min_last_week": min_last_week,
                            "best_value": current_price,
                        }
                    }
                    data_from_file.update(stock)
            json.dump(data_from_file, stock_file, indent=4)

    def update_gia_mua(self):
        response = requests.get(END_POINT, headers=HEADERS)
        response.raise_for_status()
        data_list = response.json()
        try:
            with open(FILE_NAME) as stock_file:
                data_from_file = json.load(stock_file)
        except FileNotFoundError:
            with open(FILE_NAME, "a") as stock_file:
                data_from_file = {}

        with open(FILE_NAME, 'w') as stock_file:
            for data in data_list:
                stock_code = data["_sc_"]
                if stock_code in STOCK_LIST:
                    current_price = int(data["_cp_"])
                    should_buy = data_from_file[stock_code]["should_buy"]
                    enable_sound = data_from_file[stock_code]["enable_sound"]
                    percent_cut_loss = data_from_file[stock_code]["percent_cut_loss"]
                    percent_sell = data_from_file[stock_code]["percent_sell"]
                    min_last_week = data_from_file[stock_code]["min_last_week"]
                    best_value = data_from_file[stock_code]["best_value"]
                    stock = {
                        data["_sc_"]: {
                            "should_buy": should_buy,
                            "enable_sound": enable_sound,
                            "bought": current_price,
                            "percent_cut_loss": percent_cut_loss,
                            "percent_sell": percent_sell,
                            "min_last_week": min_last_week,
                            "best_value": best_value,
                        }
                    }
                    data_from_file.update(stock)
            json.dump(data_from_file, stock_file, indent=4)
            # self.draw_body(self.frame)

    def percent_gia_tot_nhat_hien_tai(self, start_value, end_value, label: Label):
        final_value = end_value - start_value
        if final_value >= 0:
            final_value = "{:.2f}".format(final_value)
            label.config(text=f"{final_value}%", bg="#00E11A")
        else:
            final_value = "{:.2f}".format(final_value)
            label.config(text=f"{final_value}%", bg="#F33232")
        return final_value

    def format_time(self, time_value):
        min_time_this_week_value = time_value
        date = datetime.fromtimestamp(min_time_this_week_value / 1000.0)
        day_of_week = int(date.strftime("%w")) + 1
        am_pm = date.strftime("%p").lower()
        background = AM_COLOR_BACKGROUND
        if am_pm == "pm":
            background = PM_COLOR_BACKGROUND
        date_str = date.strftime(f"T{day_of_week}, %d-%m, %I:%M %p")
        return {"background": background, "time": date_str}

    def draw_header(self, frame):
        row = 1
        # Tính % thay đổi START
        percent_change_label = Label(master=frame, text="Tính % thay đổi", font=FONT_HEADER)
        percent_change_label.grid(column=1, row=row, columnspan=3)

        start_change_input = Entry(master=frame, width=ENTRY_WIDTH)
        start_change_input.grid(column=4, row=row, columnspan=2)
        self.start_change_input = start_change_input

        to_change_label = Label(master=frame, text="-", font=FONT_HEADER)
        to_change_label.grid(column=6, row=row)

        end_change_input = Entry(master=frame, width=ENTRY_WIDTH)
        end_change_input.grid(column=7, row=row, columnspan=2)
        self.end_change_input = end_change_input

        equal_button = Button(master=frame, text="  =  ", foreground="green", font=FONT_HEADER,
                              command=self.calculate_percent)
        equal_button.grid(column=9, row=row)

        percent_symbol_label = Label(master=frame, text="%", font=FONT_HEADER)
        percent_symbol_label.grid(column=10, row=row)
        self.percent_symbol_label = percent_symbol_label

        stock_code_label_header = Label(master=frame, text="Mã CK:", font=FONT_HEADER)
        stock_code_label_header.grid(column=11, row=row)

        stock_code_input_header = Entry(master=frame, width=ENTRY_WIDTH)
        stock_code_input_header.grid(column=12, row=row, columnspan=2)
        self.stock_code_input_header = stock_code_input_header

        add_to_file_button_header = Button(master=frame, text="Add", foreground="green", font=FONT_HEADER,
                                           command=self.add_stock_to_file)
        add_to_file_button_header.grid(column=14, row=row)
        # Tính % thay đổi END
        row += 1

        # Khoang cach an toàn start
        khoang_cach_an_toan_label = Label(master=frame, text="Khoảng cách an toàn:", font=FONT_HEADER)
        khoang_cach_an_toan_label.grid(column=1, row=row, columnspan=3)

        khoang_cach_an_toan_min_input = Entry(master=frame, width=ENTRY_WIDTH)
        khoang_cach_an_toan_min_input.grid(column=4, row=row, columnspan=2)
        self.khoang_cach_an_toan_min_input = khoang_cach_an_toan_min_input

        khoang_cach_an_toan_to_input = Entry(master=frame, width=ENTRY_WIDTH)
        khoang_cach_an_toan_to_input.insert(END, 4)
        khoang_cach_an_toan_to_input.grid(column=6, row=row)
        self.khoang_cach_an_toan_to_input = khoang_cach_an_toan_to_input

        khoang_cach_an_toan_max_input = Entry(master=frame, width=ENTRY_WIDTH)
        khoang_cach_an_toan_max_input.grid(column=7, row=row, columnspan=2)
        self.khoang_cach_an_toan_max_input = khoang_cach_an_toan_max_input

        khoang_cach_an_toan_cal_button = Button(master=frame, text="  =  ", foreground="green", font=FONT_HEADER,
                                                command=self.distance_value)
        khoang_cach_an_toan_cal_button.grid(column=9, row=row)
        self.khoang_cach_an_toan_cal_button = khoang_cach_an_toan_cal_button

        khoang_cach_an_toan_result_min_input = Entry(master=frame)
        khoang_cach_an_toan_result_min_input.grid(column=10, row=row, columnspan=2)
        self.khoang_cach_an_toan_result_min_input = khoang_cach_an_toan_result_min_input

        khoang_cach_an_toan_result_max_input = Entry(master=frame)
        khoang_cach_an_toan_result_max_input.grid(column=12, row=row, columnspan=2)
        self.khoang_cach_an_toan_result_max_input = khoang_cach_an_toan_result_max_input
        # Khoang cach an toàn END

        row += 1
        # Start stop START
        start_button = Button(master=frame, text="Start", foreground="green", font=FONT_HEADER,
                              command=self.start_progress)
        start_button.grid(column=1, row=row)
        self.start_button = start_button

        stop_button = Button(master=frame, text="Stop", foreground="orange", font=FONT_HEADER,
                             command=self.stop_progress)
        stop_button.grid(column=2, row=row)
        stop_button.config(state=DISABLED)
        self.stop_button = stop_button

        save_all_button = Button(master=frame, text="Save", foreground="green", font=FONT_HEADER, command=self.save_all)
        save_all_button.grid(column=3, row=row)

        status_label = Label(master=frame, text="STOPPED", foreground="red", font=FONT_HEADER)
        status_label.grid(column=4, row=row, columnspan=2)
        self.status_label = status_label
        # Start stop START
        row += 1
        # Update giá tốt nhất START
        update_gia_tot_nhat_start_button = Button(master=frame, text="Update GB", foreground="green", font=FONT_HEADER,
                                                  command=self.update_gia_tot_nhat)
        update_gia_tot_nhat_start_button.grid(column=1, row=row, columnspan=2)
        # self.start_button = start_button

        update_gia_mua_button = Button(master=frame, text="Update GM", foreground="orange", font=FONT_HEADER,
                                       command=self.update_gia_mua)
        update_gia_mua_button.grid(column=3, row=row, columnspan=2)
        update_gia_mua_button.config()
        # self.stop_button = stop_button
        # Update giá tốt nhất END

        row += 1
        # Show chart START
        show_chart_button = Button(master=frame, text="Show chart", font=FONT_HEADER, foreground=AM_COLOR_BACKGROUND,
                                   command=self.show_chart)
        show_chart_button.grid(column=1, row=row, columnspan=2)
        # Show chart STOP

        row += 1
        column = 1

        # sound
        check_value = IntVar()
        check_value.set(0)
        sound_all_checkbox = Checkbutton(master=frame, text="Sound", variable=check_value, onvalue=1, offvalue=0,
                                         font=FONT_HEADER, command=self.check_all_function)
        sound_all_checkbox.grid(column=column, row=row)
        self.check_all_checkbox = check_value

        # Mã chứng khoán
        stock_code = Label(master=frame, text="Mã ck", font=FONT_HEADER)
        column += 1
        stock_code.grid(column=column, row=row)

        # Show chart
        show_chart_label = Label(master=frame, text="Chart", font=FONT_HEADER)
        column += 1
        show_chart_label.grid(column=column, row=row)

        # Giá min tuần này
        min_value_this_week_label = Label(master=frame, text="Min t/này", font=FONT_HEADER)
        column += 1
        min_value_this_week_label.grid(column=column, row=row)

        # Thời gian giá nhỏ nhất tuần này
        min_time_this_week_label = Label(master=frame, text="Time", font=FONT_HEADER)
        column += 1
        min_time_this_week_label.grid(column=column, row=row)

        # Giá max tuần này
        max_value_this_week_label = Label(master=frame, text="Max t/này", font=FONT_HEADER)
        column += 1
        max_value_this_week_label.grid(column=column, row=row)

        # Thời gian giá lớn nhất tuần này
        max_time_this_week_label = Label(master=frame, text="Time", font=FONT_HEADER)
        column += 1
        max_time_this_week_label.grid(column=column, row=row)

        # Phần trăm giữa giá lớn nhất và nhỏ nhất
        percent_max_min_price_label = Label(master=frame, text="% Max-Min", font=FONT_HEADER)
        column += 1
        percent_max_min_price_label.grid(column=column, row=row)

        # % Cắt lỗ
        max_value = Label(master=frame, text="% Cắt lỗ", font=FONT_HEADER)
        column += 1
        max_value.grid(column=column, row=row)

        # % Bán
        min_value = Label(master=frame, text="% Bán", font=FONT_HEADER)
        column += 1
        min_value.grid(column=column, row=row)

        # Giá nên mua
        max_value = Label(master=frame, text="Giá nên mua", font=FONT_HEADER)
        column += 1
        max_value.grid(column=column, row=row)

        # Trần
        gia_tran_label = Label(master=frame, text="Trần", font=FONT_HEADER)
        column += 1
        gia_tran_label.grid(column=column, row=row)

        # Sàn
        gia_san_label = Label(master=frame, text="Sàn", font=FONT_HEADER)
        column += 1
        gia_san_label.grid(column=column, row=row)

        # "Mở cửa
        gia_mo_cua_label = Label(master=frame, text="Mở cửa", font=FONT_HEADER)
        column += 1
        gia_mo_cua_label.grid(column=column, row=row)

        # Hiện tại
        current_value_label = Label(master=frame, text="Hiện tại", font=FONT_HEADER)
        column += 1
        current_value_label.grid(column=column, row=row)

        # Giá đã mua
        gia_da_mua_label = Label(master=frame, text="Giá đã mua", font=FONT_HEADER)
        column += 1
        gia_da_mua_label.grid(column=column, row=row)

        # GTN
        gia_tot_nhat_label = Label(master=frame, text="Giá bán(GB)", font=FONT_HEADER)
        column += 1
        gia_tot_nhat_label.grid(column=column, row=row)

        # % GTN
        percent_tai_gia_tot_nhat_label = Label(master=frame, text="% GB", font=FONT_HEADER)
        column += 1
        percent_tai_gia_tot_nhat_label.grid(column=column, row=row)

        # Lãi/lỗ
        lai_lo_label = Label(master=frame, text="Lãi/lỗ", font=FONT_HEADER)
        column += 1
        lai_lo_label.grid(column=column, row=row)

        # % GTN - HT
        percent_gia_tot_nhat_hien_tai_label = Label(master=frame, text="% GTN - HT", font=FONT_HEADER)
        column += 1
        percent_gia_tot_nhat_hien_tai_label.grid(column=column, row=row)

        # Status
        radio_choose = Label(master=frame, text="Status", font=FONT_HEADER)
        column += 1
        radio_choose.grid(column=column, row=row)

        empty_label = Label(master=frame, text="        ", font=FONT_HEADER)
        column += 1
        empty_label.grid(column=column, row=row)

        global COLS
        COLS = column + 2

    def draw_body(self, frame):
        with open(FILE_NAME) as data_file:
            self.stock_code_from_file = json.load(data_file)
            global ROWS
            ROWS = len(self.stock_code_from_file)
        row = 7
        for stock_code in self.stock_code_from_file:
            item_dict = self.stock_code_from_file[stock_code]
            collection_data = self.collection_data[stock_code]
            column = 0

            # sound
            check_value = IntVar()
            check_value.set(int(item_dict.get("enable_sound")))
            stock_checkbox = Checkbutton(master=frame, variable=check_value, onvalue=1, offvalue=0)
            column += 1
            stock_checkbox.grid(column=column, row=row)
            self.item_list[f'stock_checkbox_{stock_code.lower()}'] = check_value

            # Mã chứng khoán
            stock_code_label = Label(master=frame, text=stock_code)
            column += 1
            stock_code_label.grid(column=column, row=row)

            # Show chart
            chart_value = IntVar()
            chart_value.set(0)
            show_chart_checkbox = Checkbutton(master=frame, variable=chart_value, onvalue=1, offvalue=0)
            column += 1
            show_chart_checkbox.grid(column=column, row=row)
            self.item_list[f'show_chart_checkbox_{stock_code.lower()}'] = chart_value

            # Giá nhỏ nhất tuần này
            min_value_this_week_value = collection_data["min_price"]
            min_value_this_week_label = Label(master=frame, width=ENTRY_WIDTH,
                                              text="{:,.0f}".format(min_value_this_week_value))
            column += 1
            min_value_this_week_label.grid(column=column, row=row)

            # Thời gian giá nhỏ nhất tuần này
            min_time_this_week_value = self.format_time(collection_data["min_price_time"])
            min_time_this_week_label = Label(master=frame, text=min_time_this_week_value["time"],
                                             background=min_time_this_week_value["background"])
            column += 1
            min_time_this_week_label.grid(column=column, row=row)

            # Giá max tuần này
            max_value_this_week_value = collection_data["max_price"]
            max_value_this_week_label = Label(master=frame, width=ENTRY_WIDTH,
                                              text="{:,.0f}".format(max_value_this_week_value))
            column += 1
            max_value_this_week_label.grid(column=column, row=row)

            # Thời gian giá lớn nhất tuần này
            max_time_this_week_value = self.format_time(collection_data["max_price_time"])
            max_time_this_week_label = Label(master=frame, text=max_time_this_week_value["time"],
                                             background=max_time_this_week_value["background"])
            column += 1
            max_time_this_week_label.grid(column=column, row=row)

            # Phần trăm giữa giá lớn nhất và nhỏ nhất
            percent_min_max = ((
                                       max_value_this_week_value - min_value_this_week_value) / min_value_this_week_value) * 100
            percent_max_min_price_label = Label(master=frame, text="{:.2f}".format(percent_min_max) + "%",
                                                bg=BACKGROUND_LAI)
            column += 1
            percent_max_min_price_label.grid(column=column, row=row)

            try:
                percent_cut_loss_value = float(item_dict.get("percent_cut_loss"))
            except TypeError:
                percent_cut_loss_value = float(4)
            percent_cut_loss_entry = Entry(master=frame, width=ENTRY_WIDTH)
            percent_cut_loss_entry.insert(0, percent_cut_loss_value)
            column += 1
            percent_cut_loss_entry.grid(column=column, row=row)
            self.item_list[f'percent_cut_loss_entry_{stock_code.lower()}'] = percent_cut_loss_entry

            try:
                percent_sell_value = float(item_dict.get("percent_sell"))
            except TypeError:
                percent_sell_value = float(4)
            percent_sell_entry = Entry(master=frame, width=ENTRY_WIDTH)
            percent_sell_entry.insert(0, percent_sell_value)
            column += 1
            percent_sell_entry.grid(column=column, row=row)
            self.item_list[f'percent_sell_entry_{stock_code.lower()}'] = percent_sell_entry

            min_value_entry = Entry(master=frame, width=ENTRY_WIDTH)
            min_value_entry.insert(END, item_dict.get("should_buy"))
            column += 1
            min_value_entry.grid(column=column, row=row)
            self.item_list[f'min_value_entry_{stock_code.lower()}'] = min_value_entry

            gia_tran_label = Label(master=frame, text="{:,.0f}".format(0.00))
            column += 1
            gia_tran_label.grid(column=column, row=row)
            self.item_list[f'gia_tran_label_{stock_code.lower()}'] = gia_tran_label

            gia_san_label = Label(master=frame, text="{:,.0f}".format(0.00))
            column += 1
            gia_san_label.grid(column=column, row=row)
            self.item_list[f'gia_san_label_{stock_code.lower()}'] = gia_san_label

            gia_mo_cua_label = Label(master=frame, text="{:,.0f}".format(0.00))
            column += 1
            gia_mo_cua_label.grid(column=column, row=row)
            self.item_list[f'gia_mo_cua_label_{stock_code.lower()}'] = gia_mo_cua_label

            current_value_label = Label(master=frame, text="{:,.0f}".format(0.00))
            column += 1
            current_value_label.grid(column=column, row=row)
            self.item_list[f'current_value_label_{stock_code.lower()}'] = current_value_label

            gia_da_mua_entry = Entry(master=frame, width=ENTRY_WIDTH)
            try:
                gia_da_mua = int(item_dict.get("bought"))
            except TypeError:
                gia_da_mua = 0
            gia_da_mua_entry.insert(END, gia_da_mua)
            column += 1
            gia_da_mua_entry.grid(column=column, row=row)
            self.item_list[f'gia_da_mua_entry_{stock_code.lower()}'] = gia_da_mua_entry

            try:
                gia_tot_nhat_value = int(item_dict.get("best_value"))
            except TypeError:
                gia_tot_nhat_value = 0

            percent_tai_gia_tot_value = 0
            gia_tot_nhat_entry = Entry(master=frame, width=ENTRY_WIDTH)
            gia_tot_nhat_entry.insert(END, gia_tot_nhat_value)
            column += 1
            gia_tot_nhat_entry.grid(column=column, row=row)
            self.item_list[f'gia_tot_nhat_entry_{stock_code.lower()}'] = gia_tot_nhat_entry

            percent_tai_gia_tot_nhat_entry = Label(master=frame)

            if gia_tot_nhat_value > 0:
                percent_tai_gia_tot_value = self.percent_lai_lo(gia_da_mua, gia_tot_nhat_value,
                                                                percent_tai_gia_tot_nhat_entry)
            else:
                percent_tai_gia_tot_nhat_entry.config(text="0")
            column += 1
            percent_tai_gia_tot_nhat_entry.grid(column=column, row=row)
            self.item_list[f'percent_tai_gia_tot_nhat_entry_{stock_code.lower()}'] = percent_tai_gia_tot_nhat_entry

            lai_lo_label = Label(master=frame, text="0")
            column += 1
            lai_lo_label.grid(column=column, row=row)
            self.item_list[f'lai_lo_label_{stock_code.lower()}'] = lai_lo_label

            percent_gia_tot_nhat_hien_tai_label = Label(master=frame, text=percent_tai_gia_tot_value)
            column += 1
            percent_gia_tot_nhat_hien_tai_label.grid(column=column, row=row)
            self.item_list[
                f'percent_gia_tot_nhat_hien_tai_label_{stock_code.lower()}'] = percent_gia_tot_nhat_hien_tai_label

            status_label = Label(master=frame, text=STATUS_CHECK)
            column += 1
            status_label.grid(column=column, row=row)
            self.item_list[f'status_label_{stock_code.lower()}'] = status_label
            row += 1

    def draw_table(self, frame):
        self.draw_header(frame)
        self.draw_body(frame)

    def show_chart(self):
        self.get_data_from_collection()
        check_exist = False
        for stock_code in self.stock_code_from_file:
            check_value = self.item_list[f'show_chart_checkbox_{stock_code.lower()}'].get()
            if check_value == 1:
                check_exist = True
                list_data = self.collection_data[stock_code]
                data = list_data["line_price_2"] + list_data["line_price_3"] + list_data["line_price_4"] + list_data[
                    "line_price_5"] + list_data["line_price_6"]
                dx = [self.format_time(item["time"])["time"] for item in data]
                dy = [item["price"] for item in data]
                fig = go.Figure([go.Scatter(x=dx, y=dy)])
                fig.show()
                break
        if not check_exist:
            tkinter.messagebox.showerror("Error", "Tại colum 'Chart' vui lòng check ít nhất 1 record")