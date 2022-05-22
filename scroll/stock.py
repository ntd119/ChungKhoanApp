import pandas
from tkinter import *
import requests
import winsound
from datetime import datetime, time
import tkinter.messagebox
import json

FILE_NAME = "./data/stock-code.json"
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
PERCENT_DESIRE = 4
BACKGROUND_COLOR = "#F0F0F0"

ROWS, COLS = 20, 10
ROWS_DISP = 15
COLS_DISP = 10



class Stock(Tk):
    def __init__(self, title='Hội Phá Đảo CK', *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

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
        self.draw_table(frame)
        canvas.create_window((0, 0), window=frame, anchor=NW)

        frame.update_idletasks()
        bbox = canvas.bbox(ALL)

        w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
        dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
        canvas.configure(scrollregion=bbox, width=dw, height=dh)

    def draw_header(self, frame):
        row = 1
        column = 1

        # sound
        check_value = IntVar()
        check_value.set(0)
        sound_all_checkbox = Checkbutton(master=frame, text="Sound", variable=check_value, onvalue=1, offvalue=0,
                                         font=FONT_HEADER)
        sound_all_checkbox.grid(column=column, row=row)
        # self.check_all_checkbox = check_value

        # Mã chứng khoán
        stock_code = Label(master=frame, text="Mã ck", font=FONT_HEADER)
        column += 1
        stock_code.grid(column=column, row=row)

        # Giá min tuần trước
        min_value_last_week_label = Label(master=frame, text="Min t/trước", font=FONT_HEADER)
        column += 1
        min_value_last_week_label.grid(column=column, row=row)

        # % Cắt lỗ
        max_value = Label(master=frame, text="% Cắt lỗ", font=FONT_HEADER)
        column += 1
        max_value.grid(column=column, row=row)

        # % Bán
        min_value = Label(master=frame, text="% Bán", font=FONT_HEADER)
        column += 1
        min_value.grid(column=column, row=row)

        # Giá nên mua
        max_value = Label(master=frame,text="Giá nên mua", font=FONT_HEADER)
        column += 1
        max_value.grid(column=column, row=row)

        # Trần
        gia_tran_label = Label(master=frame,text="Trần", font=FONT_HEADER)
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
        gia_tot_nhat_label = Label(master=frame, text="GTN", font=FONT_HEADER)
        column += 1
        gia_tot_nhat_label.grid(column=column, row=row)

        # % GTN
        percent_tai_gia_tot_nhat_label = Label(master=frame, text="% GTN", font=FONT_HEADER)
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

    def draw_body(self, frame):
        with open(FILE_NAME) as data_file:
            stock_code_from_file = json.load(data_file)
        row = 2
        for stock_code in stock_code_from_file:
            item_dict = stock_code_from_file[stock_code]
            column = 0

            # sound
            check_value = IntVar()
            check_value.set(int(item_dict.get("enable_sound")))
            stock_checkbox = Checkbutton(master=frame, variable=check_value, onvalue=1, offvalue=0)
            column += 1
            stock_checkbox.grid(column=column, row=row)

            # self.item_list[f'stock_checkbox_{stock_code.lower()}'] = check_value

            # Mã chứng khoán
            stock_code_label = Label(master=frame, text=stock_code)
            column += 1
            stock_code_label.grid(column=column, row=row)

            try:
                min_value_last_week_value = int(item_dict.get("min_last_week"))
            except TypeError:
                min_value_last_week_value = 0
            min_value_last_week_entry = Entry(master=frame, width=ENTRY_WIDTH)
            min_value_last_week_entry.insert(END, min_value_last_week_value)
            column += 1
            min_value_last_week_entry.grid(column=column, row=row)
            self.item_list[f'min_value_last_week_entry_{stock_code.lower()}'] = min_value_last_week_entry

            try:
                percent_cut_loss_value = float(item_dict.get("percent_cut_loss"))
            except TypeError:
                percent_cut_loss_value = float(4)
            percent_cut_loss_entry = Entry(master= frame, width=ENTRY_WIDTH)
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

            current_value_label = Label(master= frame, text="{:,.0f}".format(0.00))
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


