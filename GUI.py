from tkinter import *
import requests
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
GIA_TRAN = "Giá trần: "
GIA_SAN = "Giá sàn: "
GIA_MO_CUA = "Giá mở cửa: "
GIA_MOI_NHAT = "Giá mới nhất: "
END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2?sectorID=0&catID=0&capitalID=0&languageID=1"
error = ""
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
# ---------------------------- TIMER RESET ------------------------------- #
def get_api_data():
    error = ""
    response = requests.get(url=END_POINT, headers=HEADERS)
    if response.status_code != 200:
        error = "Error"
    else:
        json_data = response.json()
        filter_list = [row for row in json_data if row["_sc_"] == "VCB"]
        if len(filter_list) == 1:
            dict_data = filter_list[0]
            # Giá trần: _clp_
            gia_tran.config(text=f"{GIA_TRAN} {dict_data['_clp_']}")
            # Giá sàn: _fp_
            gia_san.config(text=f"{GIA_SAN} {dict_data['_fp_']}")
            # Giá mở cửa: _op_
            gia_mo_cua.config(text=f"{GIA_MO_CUA} {dict_data['_fp_']}")
            # Giá mới nhất: _cp_
            gia_moi_nhat.config(text=f"{GIA_MOI_NHAT} {dict_data['_cp_']}")
            window.after(10000, get_api_data)
        else:
            error = "Lỗi dữ liệu có nhiều hơn 1 dòng"

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MTD TEAM")
window.config(padx=100, pady=50, bg=YELLOW)

timer_lable = Label(text="MTD Team", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
timer_lable.grid(column=1, row=0)

canvas = Canvas(width=200, height=133, background=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="chung-khoan.png")
canvas.create_image(100, 66, image=tomato_img)
canvas.grid(column=1, row=1)


code_ck = Entry()
code_ck.insert(END, "VCB")
code_ck.grid(column=1, row=2)

start_button = Button(text="Start", highlightthickness=0, command=get_api_data)
start_button.grid(column=0, row=2)

end_button = Button(text="End", highlightthickness=0)
end_button.grid(column=2, row=2)

gia_tran = Label(text=GIA_TRAN, fg="black", bg=YELLOW, font=(FONT_NAME, 15, "bold"))
gia_tran.grid(column=1, row=3)

gia_san = Label(text=GIA_SAN, fg="black", bg=YELLOW, font=(FONT_NAME, 15, "bold"))
gia_san.grid(column=1, row=4)

gia_mo_cua = Label(text=GIA_MO_CUA, fg="black", bg=YELLOW, font=(FONT_NAME, 15, "bold"))
gia_mo_cua.grid(column=1, row=5)

gia_moi_nhat = Label(text="Giá mới nhất: ", fg="black", bg=YELLOW, font=(FONT_NAME, 15, "bold"))
gia_moi_nhat.grid(column=1, row=6)


window.mainloop()