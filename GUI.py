from tkinter import *

import pandas

root = Tk()
root.title("MTD Team")
root.config(width=800, height=400)

data = pandas.read_csv("./file/stock-code.csv")
# stock_code_dict = data.to_dict()
# print(stock_code_dict)

for (index, row) in data.iterrows():
    print(row["min"])

# print(data)
# stock_code_list = data.to_dict()
#
# print(type(stock_code_list))

# for i in stock_code_list:
#     stock_code = stock_code_list[i]
#     print(stock_code)




root.mainloop()