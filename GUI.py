from tkinter import *

import pandas

root = Tk()
root.title("MTD Team")
root.config(width=800, height=400)

data = pandas.read_csv("./file/stock-code.csv")
stock_code = data.to_dict()["code"]



print(stock_code)




root.mainloop()