from tkinter import *
from stock import Stock

root = Tk()
root.title("MTD Team")
root.config(width=800, height=400)
stock = Stock()

print (stock.stock_code_list)
stock.draw_header()






root.mainloop()