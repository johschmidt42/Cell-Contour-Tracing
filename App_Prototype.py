import os
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename, askdirectory

import numpy as np
from skimage.filters import gaussian
from skimage.io import imread, imsave

from Tooltip import createToolTip

# This Application uses Tkinter for creating a GUI.
# The class App creates the window Tk and also creates the Pages of that window.
# Fonts are stored here. There is a font chooser function that returns the fonts code.

LARGE_FONT = ("Verdana", 12)


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.frames = {}

        for F in (StartPage,
                  PageOne):
            # PageOne is simply a placeholder in case other Pages need to be added later on.
            # Pages need to be added here manually. Access to the Objects through App.frames[index].
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)  # Shows the StartPage, whenever the program starts

    def show_frame(self, context):  # method to show the needed page on the window Tk (e.g. when clicked on a button)
        frame = self.frames[context]
        frame.tkraise()


class StartPage(LabelFrame):  # MainPage
    def __init__(self, parent):
        LabelFrame.__init__(self, parent)  # MainFrame of the Page

        # Variables
        self.rb = IntVar()
        self.rb.set(0)

        self.filename = StringVar()
        self.filename.set("No File Selected")

        self.filedirectory = StringVar()
        self.filedirectory.set("No Directory Selected")

        # Initialising Frames within the MainFrame for organisational purposes

        self.frame1 = LabelFrame(self)
        self.frame2 = Frame(self)
        self.frame3 = LabelFrame(self, text="Select filter")
        self.frame4 = Frame(self)
        self.frame5 = Frame(self)

        # Placing Frames within the MainFrame

        self.frame1.grid(row=0, column=0, pady=10, padx=10)
        self.frame2.grid(row=0, column=1, pady=10, padx=10)
        self.frame3.grid(row=1, column=0, pady=10, padx=10)
        self.frame4.grid(row=1, column=1, pady=10, padx=10)
        self.frame5.grid(row=0, column=2, pady=10, padx=10, rowspan=2)

        # Initialising Lables

        self.l1 = Label(self.frame2, textvariable=self.filename)
        self.l2 = Label(self.frame2, textvariable=self.filedirectory)
        self.l3 = Label(self.frame2, text="This file will be used: ", font=LARGE_FONT)
        self.l4 = Label(self.frame2, text="The file will be saved in this directory: ", font=LARGE_FONT)

        # Placing Lables

        self.l1.grid(row=1, column=0, sticky="w")
        self.l2.grid(row=3, column=0, sticky="w")
        self.l3.grid(row=0, column=0, sticky="w")
        self.l4.grid(row=2, column=0, sticky="w")

        # Initialising Buttons

        self.b1 = Button(self.frame1, text="Select File", command=self.getfilename, width=20)
        self.b2 = Button(self.frame1, text="Select Folder", command=self.getdirectory, width=20)
        self.b3 = Button(self.frame4, text="Execute", command=self.operation, width=20, height=2)

        createToolTip(self.b1, "This is a tooltip.")

        # Placing Buttons

        self.b1.pack(fill=BOTH, pady=5, padx=5)
        self.b2.pack(fill=BOTH, pady=5, padx=5)
        self.b3.pack(fill=BOTH)

        # Initialising Radiobuttons

        self.rb1 = Radiobutton(self.frame3, text="Gaussian Filter", variable=self.rb, value=0)

        # Placing Radiobuttons

        self.rb1.grid(row=0, sticky="w")

    # Instancemethods

    def getfilename(self):
        fname = askopenfilename(title="Select file",
                                filetypes=(("tif files", "*.tif"), ("all files", "*.*")))  # Opens file open dialog
        if fname:
            self.filename.set(fname)  # filename variable receives the string of the OpenFile Dialog

    def getdirectory(self):
        fdir = askdirectory()  # Opens Directory open dialog
        if fdir:
            self.filedirectory.set(fdir)  # filedirectory variable receives the string of the open Directory dialog

    def operation(self):
        if self.rb.get() == 0:  # First Radiobutton is clicked
            new_windowGauss(self)  # Creates the Gausswindow
            app.withdraw()  # MainWindow (Tk) is withdrawn
        else:
            print("Fehler")


class PageOne(Frame):  # Other Frame
    def __init__(self, parent):
        LabelFrame.__init__(self, parent)


class WindowGauss:
    def __init__(self, parent):
        self.parent = parent

        self.frame1 = Frame(parent)
        self.frame1.grid(row=0, column=0, pady=10, padx=10, columnspan=2)
        self.frame2 = Frame(parent)
        self.frame2.grid(row=1, column=0, pady=10, padx=10)
        self.frame3 = Frame(parent)
        self.frame3.grid(row=1, column=1, pady=10, padx=10)
        self.frame4 = Frame(parent)
        self.frame4.grid(row=2, column=0, pady=10, padx=10, columnspan=2)

        self.l1Gau = Label(self.frame1, text="Sigma: ", font=LARGE_FONT)
        self.l1Gau.pack(side="left")

        self.e1Gau = Entry(self.frame1, width=3)
        self.e1Gau.pack(side="left")

        self.b1Gau = Button(self.frame2, text="OK", width=20, font=LARGE_FONT, command=self.ExecuteGaussAndClose)
        self.b1Gau.pack(side="left", padx=10)
        self.b2Gau = Button(self.frame2, text="Cancel", width=20, font=LARGE_FONT, command=self.close_windows)
        self.b2Gau.pack(side="left", padx=10)

        self.rbGau = IntVar()
        self.rbGau.set(2)

        self.rb1Gau = Radiobutton(self.frame1, text="reflect", variable=self.rbGau, value=0)
        self.rb2Gau = Radiobutton(self.frame1, text="constant", variable=self.rbGau, value=1)
        self.rb3Gau = Radiobutton(self.frame1, text="nearest (default)", variable=self.rbGau, value=2)
        self.rb4Gau = Radiobutton(self.frame1, text="mirror", variable=self.rbGau, value=3)
        self.rb5Gau = Radiobutton(self.frame1, text="wrap", variable=self.rbGau, value=4)

        self.rb1Gau.pack(padx=20, anchor="w")
        self.rb2Gau.pack(padx=20, anchor="w")
        self.rb3Gau.pack(padx=20, anchor="w")
        self.rb4Gau.pack(padx=20, anchor="w")
        self.rb5Gau.pack(padx=20, anchor="w")

        self.pgb = ttk.Progressbar(self.frame4, orient='horizontal', mode='determinate', length=200)
        self.pgb.pack(expand=True, fill=BOTH, side=TOP)

    def close_windows(self):
        self.parent.destroy()
        app.deiconify()

    def ExecuteGaussAndClose(self):
        if app.frames[StartPage].filename.get() == "No File Selected":
            messagebox.showerror("File", "No file selected")
        elif app.frames[StartPage].filename.get()[-3:] != "tif":
            messagebox.showerror("File Format", "File is not a .tif file!")
        elif self.e1Gau.get() == "":
            messagebox.showerror("Sigma", "Please type in a Sigma value!")
        elif int(self.e1Gau.get()) < 0:
            messagebox.showerror("Sigma", "Sigma is out of range")
        else:
            if app.frames[StartPage].filedirectory.get() == "No Directory Selected":
                messagebox.showerror("Directory", "No Directory Selected")
            else:
                self.pgb["value"] = 0
                array = imread(app.frames[StartPage].filename.get())
                self.pgb["value"] = 10
                messagebox.showinfo("", "Reading Image successful")
                if self.rbGau.get() == 0:
                    gaussianMode = "reflect"
                if self.rbGau.get() == 1:
                    gaussianMode = "constant"
                if self.rbGau.get() == 2:
                    gaussianMode = "nearest"
                if self.rbGau.get() == 3:
                    gaussianMode = "mirror"
                if self.rbGau.get() == 4:
                    gaussianMode = "wrap"

                newArray = gaussian(array, sigma=int(self.e1Gau.get()), preserve_range=True, mode=gaussianMode)
                self.pgb["value"] = 30
                messagebox.showinfo("", "Prozess abgeschlossen mit Sigma %d" % (int(self.e1Gau.get())))

                completeFilename = app.frames[StartPage].filename.get()
                filenameWithoutEnding = completeFilename.split(".")[-2]
                filename = filenameWithoutEnding.split("/")[-1]
                filenameExtended = filename + "_gaussian_sigma=" + self.e1Gau.get() + "_mode=" + gaussianMode + ".tif"
                savedir_filename = os.path.join(app.frames[StartPage].filedirectory.get(), filenameExtended)

                imsave(savedir_filename, np.uint8(newArray))
                self.pgb["value"] = 100

                messagebox.showinfo("", "Operation completed!")
                self.close_windows()


def new_windowGauss(parent):
    new_window = Toplevel(parent)
    WiG = WindowGauss(new_window)


app = App()
app.title("Filter Application")

app.mainloop()
