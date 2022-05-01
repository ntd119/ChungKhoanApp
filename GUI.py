from tkinter import *
from stock import Stock

root = Tk()
root.title("MTD Team")
root.config(padx=50, pady=50, width=800, height=400)
stock = Stock(root)

stock.draw_header()
stock.draw_body()




root.mainloop()