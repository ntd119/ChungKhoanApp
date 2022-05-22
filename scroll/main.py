from tkinter import *

ROWS, COLS = 1, 1
ROWS_DISP = 10
COLS_DISP = 10


class MyApp(Tk):
    def __init__(self, title='Sample App', *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        master_frame = Frame(self, bd=3, relief=RIDGE)
        master_frame.grid(sticky=NSEW)
        master_frame.columnconfigure(0, weight=1)

        label1 = Label(master_frame, text='Frame1 Contents')
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

        buttons_frame = Frame(canvas)

        button = Button(master=buttons_frame, padx=7, pady=7, relief=RIDGE,
                        activebackground='orange', text='text ')
        button.grid(row=1, column=1, sticky='news')

        button1 = Button(master=buttons_frame, padx=7, pady=7, relief=RIDGE,
                        activebackground='orange', text='text ')
        button1.grid(row=1, column=2, sticky='news')

        canvas.create_window((0, 0), window=buttons_frame, anchor=NW)

        buttons_frame.update_idletasks()
        bbox = canvas.bbox(ALL)

        w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
        dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
        canvas.configure(scrollregion=bbox, width=dw, height=dh)


if __name__ == '__main__':
    app = MyApp('Scrollable Canvas')
    app.mainloop()
