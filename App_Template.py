from tkinter import Tk, Frame, IntVar, Radiobutton, Button, Toplevel


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.frames = {}
        for F in (StartPage, PageOne):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.rb = IntVar()
        self.rb.set(0)

        self.rb1 = Radiobutton(self, text="X", variable=self.rb, value=0)
        self.rb2 = Radiobutton(self, text="Y", variable=self.rb, value=1)

        self.rb1.pack()
        self.rb2.pack()

        self.page_one_button = Button(self, text="Next Page", command=self.operation)
        self.page_one_button.pack()

    def operation(self):
        if self.rb.get() == 0:
            print("You chose X")
            new_window(self)
            app.withdraw()
        elif self.rb.get() == 1:
            print("You chose Y")
            app.show_frame(PageOne)
        else:
            print("Error")


class PageOne(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        OK_button = Button(self, text="OK", width=20, command=ok_Action)
        OK_button.pack()

        start_page_button = Button(self, text="Back", width=20, command=lambda: parent.show_frame(StartPage))
        start_page_button.pack()


class WindowX:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.quitButton = Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.parent.destroy()
        app.deiconify()


def ok_Action():
    if app.frames[StartPage].rb.get() == 0:
        print("Calculate with X")
    elif app.frames[StartPage].rb.get() == 1:
        print("Calculate with X")
    else:
        print("Error")


def new_window(parent):
    new_window = Toplevel(parent)
    WiX = WindowX(new_window)


app = App()
app.mainloop()
