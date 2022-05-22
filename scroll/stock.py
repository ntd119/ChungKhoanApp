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
PERCENT_DESIRE = 4
BACKGROUND_COLOR = "#F0F0F0"

ROWS, COLS = 5, 10
ROWS_DISP = 16
COLS_DISP = 10



class Stock(Tk):
    def __init__(self, title='Hội Phá Đảo CK', *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

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


    def draw_table(self, frame):
        self.draw_header(frame)
