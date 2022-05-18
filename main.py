from tkinter import *
from stock import Stock

root = Tk()
# w.pack()

# scroll_bar = Scrollbar(root)
#
# scroll_bar.pack(side=RIGHT,
#                 fill=Y)

root.title("MTD Team")
stock = Stock(root)
root.config(padx=50, pady=50, width=800, height=400, bg=stock.background_color)
stock.draw_header()
stock.draw_body()
root.mainloop()