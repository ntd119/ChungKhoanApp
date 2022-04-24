import random
from tkinter import *
import requests
from playsound import playsound
import winsound
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
AUDIO_SPEED = "speech.mp3"
GIA_TRAN = "Giá trần: "
GIA_SAN = "Giá sàn: "
GIA_MO_CUA = "Giá mở cửa: "
GIA_MOI_NHAT = "Giá mới nhất: "
DELAY_TIME = 1000
END_POINT = "https://api.vietstock.vn/finance/sectorInfo_v2?sectorID=0&catID=0&capitalID=0&languageID=1"
error = ""
HEADERS = {"X-Requested-With": "XMLHttpRequest",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           }
# ---------------------------- TIMER RESET ------------------------------- #
# playsound(AUDIO_SPEED)
end_call_api = False
def play_sound():
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

def get_api_data():
    global end_call_api
    error = ""
    response = requests.get(url=END_POINT, headers=HEADERS)
    if response.status_code != 200:
        error = "Error"
    elif end_call_api:
        error = "STOP"
        end_call_api = False
    else:
        json_data = response.json()
        filter_list = [row for row in json_data if row["_sc_"] == code_ck.get().upper()]
        if len(filter_list) == 1:
            dict_data = filter_list[0]
            # Giá trần: _clp_
            gia_tran.config(text=f"{GIA_TRAN} {dict_data['_clp_']}")
            # Giá sàn: _fp_
            gia_san.config(text=f"{GIA_SAN} {dict_data['_fp_']}")
            # Giá mở cửa: _op_
            gia_mo_cua.config(text=f"{GIA_MO_CUA} {dict_data['_op_']}")
            # Giá mới nhất: _cp_
            get_gia_moi_nhat = dict_data['_cp_']
            gia_moi_nhat.config(text=f"{GIA_MOI_NHAT} {get_gia_moi_nhat}")
            print(random.randint(0, 100))
            convert_gia_moi_nhat = float(get_gia_moi_nhat)
            convert_gia_tri_mong_muon = float(gia_tri_mong_muon_input.get())
            value = int(radio_button_value.get())
            if value == 1:
                # Bán
                if convert_gia_moi_nhat >= convert_gia_tri_mong_muon:
                    play_sound()
            else:
                # Mua
                if convert_gia_moi_nhat <= convert_gia_tri_mong_muon:
                    play_sound()
            window.after(DELAY_TIME, get_api_data)
        else:
            error = "Lỗi dữ liệu có nhiều hơn 1 dòng"

        if not end_call_api:
            start_button.config(state=DISABLED)
            end_button.config(state=NORMAL)
        else:
            start_button.config(state=NORMAL)
            end_button.config(state=DISABLED)

def stop_call():
    global end_call_api
    end_call_api = True
    start_button.config(state=NORMAL)
    end_button.config(state=DISABLED)

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

input_ck_label = Label(text="Vui lòng nhập mã ck", fg="black", bg=YELLOW, font=(FONT_NAME, 15, "bold"))
input_ck_label.grid(column=1, row=2)

code_ck = Entry()
code_ck.insert(END, "VCB")
code_ck.grid(column=1, row=3)

start_button = Button(text="Start", highlightthickness=0,  command=get_api_data)
start_button.grid(column=0, row=3)

end_button = Button(text="End", highlightthickness=0, state=DISABLED, command=stop_call)
end_button.grid(column=2, row=3)

gia_tri_mong_muon = Label(text="Giá trị mong muốn", fg="black", bg=YELLOW, font=(FONT_NAME, 10, "normal"))
gia_tri_mong_muon.grid(column=0, row=4)

gia_tri_mong_muon_input = Entry()
gia_tri_mong_muon_input.insert(END, "83000")
gia_tri_mong_muon_input.grid(column=1, row=4)

radio_button_value = StringVar()
# initialize
radio_button_value.set(1)
R1 = Radiobutton(variable=radio_button_value, value=1, text=">=(Greater than or equal to)", bg=YELLOW)
R1.grid(column=1, row=5)

R2 = Radiobutton(variable=radio_button_value, value=2, text="<=(Less than or equal to)", bg=YELLOW)
R2.grid(column=1, row=6)

# checkbox = Checkbutton(window, text='Hiển thị thông báo',variable=100, onvalue=1, offvalue=0, bg=YELLOW)
# checkbox.grid(column=1, row=7)


gia_tran = Label(text=GIA_TRAN, fg="black", bg=YELLOW, font=(FONT_NAME, 15, "bold"))
gia_tran.grid(column=1, row=8)

gia_san = Label(text=GIA_SAN, fg="black", bg=YELLOW, font=(FONT_NAME, 15, "bold"))
gia_san.grid(column=1, row=9)

gia_mo_cua = Label(text=GIA_MO_CUA, fg="black", bg=YELLOW, font=(FONT_NAME, 15, "bold"))
gia_mo_cua.grid(column=1, row=10)

gia_moi_nhat = Label(text="Giá mới nhất: ", fg="black", bg=YELLOW, font=(FONT_NAME, 15, "bold"))
gia_moi_nhat.grid(column=1, row=11)


window.mainloop()