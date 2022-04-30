from tkinter import *

import pandas

root = Tk()
root.title("MTD Team")
root.config(width=800, height=400)

data = pandas.read_csv("./file/stock-code.csv")
stock_code_list = data.to_dict()["code"]

for i in stock_code_list:
    stock_code = stock_code_list[i]
    print(stock_code)




root.mainloop()