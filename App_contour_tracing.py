"""
The module TkinterDnD2 is needed for the app to work. The package can be found here:
http://tkinterdnd.sourceforge.net/

First download the binaries here:
https://sourceforge.net/projects/tkdnd/files/

Copy the tkdnd2.8 folder to the library folder of your enviroment - "...Env/lib/"

Then download the package here:
https://sourceforge.net/projects/tkinterdnd/files/

Copy the TkinterDnD-0.3 folder to your site-packages folder - "...Env/lib/python3.6/site-packages/"

If you are using PyCharm, add TkinterDnd-0.3 to your modules manually by adding the path of the folder.

And here is a StackOverFlow post on how to install it:
https://stackoverflow.com/questions/25427347/how-to-install-and-use-tkdnd-with-python-2-7-tkinter-on-osx
"""

import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory, askopenfilenames

import numpy as np
from PIL import Image, ImageTk
from skimage.filters import gaussian
from skimage.io import imsave, imread

"""The heart of the app"""


class App(Tk):
    """This class is the heart of the app. Every Widget can be seen, accessed from every frame."""

    def __init__(self, *args, **kwargs):
        super(App, self).__init__()
        """Making the root window stretchable"""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        """Creating the Layout/Variables etc."""
        self.createVariables()
        self.createMenuBar()
        self.createStatusbar()
        self.createScale()

        """Creating the frames"""
        self.frames = {}

        for F in (StartPage, Filters, GaussianFilter,
                  ViewAsWindows):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        self.title("Image App")

    def createMenuBar(self):
        """Creating a simple Menubar at the topleft corner"""
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=False)

        self.filemenu.add_command(label="Select Files...",
                                  command=lambda: self.getfilenames())
        self.filemenu.add_command(label="Clear", command=lambda: self.clear())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.config(menu=self.menubar)

    def show_frame(self, context):
        """Frame organisation"""
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[context]
        frame.grid()
        frame.winfo_toplevel().geometry("")

    def createImageLists(self, size, list):
        for element in list:
            self.imgArray = imread(element)
            """Check the dimensions and mode of each image"""
            if self.imgArray.ndim == 2 or Image.open(element).mode == 'RGB':
                self.img = Image.open(element)
                self.img.thumbnail(size, Image.ANTIALIAS)
                self.FilenameObjectsList_PIL.append(self.img)
                self.imageTk = ImageTk.PhotoImage(self.img)
                self.FilenameObjectsList_Tk.append(self.imageTk)
            if self.imgArray.ndim == 3 and Image.open(element).mode != 'RGB':
                self.Slices_List_PIL = []
                for Slice in range(0, self.imgArray.shape[0]):
                    self.img = Image.fromarray(np.uint8(self.imgArray[Slice, :, :]))
                    self.img.thumbnail(size, Image.ANTIALIAS)
                    self.Slices_List_PIL.append(self.img)
                self.Slices_List_Tk = [ImageTk.PhotoImage(i) for i in self.Slices_List_PIL]

                self.FilenameObjectsList_PIL.append(self.Slices_List_PIL)
                self.FilenameObjectsList_Tk.append(self.Slices_List_Tk)

    def changeImage(self, x):
        self.ImageNumberVar.set(x)

        if type(self.FilenameObjectsList_Tk[self.ImageNumberVar.get()]) == list:

            self.Canva.itemconfig(self.image_on_canvas,
                                  image=self.FilenameObjectsList_Tk[self.ImageNumberVar.get()][0])
            self.Canva.config(height=self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[1],
                              width=self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[0])

            self.butt1_window = self.Canva.create_window(
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[0] - 80,
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[1] - 25,
                anchor=NW,
                window=self.butt1)
            self.butt2_window = self.Canva.create_window(
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[0] - 165,
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[1] - 25, anchor=NW,
                window=self.butt2)
            self.updateScale(x)


        else:
            self.Canva.itemconfig(self.image_on_canvas,
                                  image=self.FilenameObjectsList_Tk[self.ImageNumberVar.get()])
            self.Canva.config(height=self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[1],
                              width=self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[0])

            self.butt1_window = self.Canva.create_window(
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[0] - 80,
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[1] - 25,
                anchor=NW,
                window=self.butt1)
            self.butt2_window = self.Canva.create_window(
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[0] - 165,
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[1] - 25, anchor=NW,
                window=self.butt2)
            try:
                self.regler.grid_forget()
            except AttributeError:
                pass

        """Update"""
        self.updateCanvasButtons()
        self.updateFilename()
        self.updateStatusbar()

    def updateStatusbar(self):
        self.label.set("Image(s): " + self.FilenameList[self.ImageNumberVar.get()].split("/")[-1].split("\\")[-1])

    def updateFilename(self):
        if len(self.FilenameList) == 1:
            self.filemenu.entryconfig(0, label="Select Files..." + " | " + self.FilenameList[
                self.ImageNumberVar.get()])
        if len(self.FilenameList) > 1:
            self.filemenu.entryconfig(0, label="Select Files..." + " | " + self.FilenameList[
                self.ImageNumberVar.get()] + " ... + " + str(
                len(self.FilenameList) - 1))

    def updateScale(self, y):
        try:
            self.regler.grid_forget()
        except AttributeError:
            pass
        self.regler.grid(row=3, sticky="nsew")
        self.regler['to'] = len(self.FilenameObjectsList_PIL[y])

    def updateCanvasButtons(self):
        if self.ImageNumberVar.get() > 0 and self.ImageNumberVar.get() != len(self.FilenameList) - 1:
            self.butt1['state'] = 'normal'
            self.butt2['state'] = 'normal'
        if self.ImageNumberVar.get() == 0 and len(self.FilenameList) - 1 != 0:
            self.butt1['state'] = 'normal'
            self.butt2['state'] = 'disabled'
        if self.ImageNumberVar.get() == len(self.FilenameList) - 1:
            self.butt1['state'] = 'disabled'
            self.butt2['state'] = 'normal'
        if len(self.FilenameList) - 1 == 0:
            self.butt1['state'] = 'disabled'
            self.butt2['state'] = 'disabled'

    def getfilenames(self):
        """The function for 'Files ...' """

        """Open Directory"""
        fname = askopenfilenames(title="Select files",
                                 filetypes=(("all files", "*.*"), ("tif files", "*.tif")))

        """Creating the filesname list"""
        self.FilenameList = [i for i in fname]

        """Resetting the FileObjectLists for Canvas"""
        self.FilenameObjectsList_PIL = []
        self.FilenameObjectsList_Tk = []

        """Creating the images and saving as objects"""
        self.size = 400, 400
        self.createImageLists(self.size, self.FilenameList)

        """Check if Canva already exists"""
        if hasattr(self, 'Canva') == False:
            self.createCanvas()
            self.updateCanvasButtons()
        if hasattr(self, 'Canva') == True:
            self.changeImage(0)
            self.updateCanvasButtons()

    def clear(self):
        """Reset everything"""
        try:
            self.Canva.destroy()
            del self.Canva
        except AttributeError:
            pass

        self.FilenameList = []
        self.FilenameObjectsList_PIL = []
        self.FilenameObjectsList_Tk = []
        self.resultList_ViewAsWindows = []
        self.filemenu.entryconfig(0, label="Select Files...")
        self.label.set("Image(s): ")

    def clear(self):
        """Reset everything"""
        try:
            self.Canva.destroy()
            del self.Canva
        except AttributeError:
            pass

        self.FilenameList = []
        self.FilenameObjectsList_PIL = []
        self.FilenameObjectsList_Tk = []
        self.resultList_ViewAsWindows = []
        self.filemenu.entryconfig(0, label="Select Files...")
        self.label.set("Image(s): ")

    def createCanvas(self):
        if type(self.FilenameObjectsList_PIL[0]) == list:
            self.Canva = Canvas(self, width=self.FilenameObjectsList_PIL[0][0].size[0],
                                height=self.FilenameObjectsList_PIL[0][0].size[1])
            self.Canva.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            self.image_on_canvas = self.Canva.create_image(0 + 2, 0 + 2, image=self.FilenameObjectsList_Tk[0][0],
                                                           anchor=NW)

            self.ImageNumberVar.set(self.FilenameObjectsList_Tk.index(self.FilenameObjectsList_Tk[0]))
            self.Canva.config(height=self.FilenameObjectsList_PIL[0][0].size[1],
                              width=self.FilenameObjectsList_PIL[0][0].size[0])

            """Create Buttons for Canvas"""
            self.butt1 = Button(self, text="Next", command=self.nextButtonCanvas, width=10, height=1)
            self.butt1_window = self.Canva.create_window(self.FilenameObjectsList_PIL[0][0].size[0] - 80,
                                                         self.FilenameObjectsList_PIL[0][0].size[1] - 25, anchor=NW,
                                                         window=self.butt1)
            self.butt2 = Button(self, text="Back", command=self.backButtonCanvas, width=10, height=1)
            self.butt2_window = self.Canva.create_window(self.FilenameObjectsList_PIL[0][0].size[0] - 165,
                                                         self.FilenameObjectsList_PIL[0][0].size[1] - 25, anchor=NW,
                                                         window=self.butt2)

            self.updateScale(self.ImageNumberVar.get())


        else:
            self.Canva = Canvas(self, width=self.FilenameObjectsList_PIL[0].size[0],
                                height=self.FilenameObjectsList_PIL[0].size[1])
            self.Canva.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            self.image_on_canvas = self.Canva.create_image(0 + 2, 0 + 2, image=self.FilenameObjectsList_Tk[0],
                                                           anchor=NW)

            self.ImageNumberVar.set(self.FilenameObjectsList_Tk.index(self.FilenameObjectsList_Tk[0]))
            self.Canva.config(height=self.FilenameObjectsList_PIL[0].size[1],
                              width=self.FilenameObjectsList_PIL[0].size[0])

            """Create Buttons for Canvas"""
            self.butt1 = Button(self, text="Next", command=self.nextButtonCanvas, width=10, height=1)
            self.butt1_window = self.Canva.create_window(self.FilenameObjectsList_PIL[0].size[0] - 80,
                                                         self.FilenameObjectsList_PIL[0].size[1] - 25, anchor=NW,
                                                         window=self.butt1)
            self.butt2 = Button(self, text="Back", command=self.backButtonCanvas, width=10, height=1)
            self.butt2_window = self.Canva.create_window(self.FilenameObjectsList_PIL[0].size[0] - 165,
                                                         self.FilenameObjectsList_PIL[0].size[1] - 25, anchor=NW,
                                                         window=self.butt2)

        """Update"""
        self.updateFilename()
        self.updateStatusbar()

    def nextButtonCanvas(self):
        self.changeImage(self.ImageNumberVar.get() + 1)
        self.updateCanvasButtons()

    def backButtonCanvas(self):
        self.changeImage(self.ImageNumberVar.get() - 1)
        self.updateCanvasButtons()

    def createScale(self):
        """Creates and shows a scale if the opened Image is a stack"""
        self.regler = Scale(self, from_=1, to=100, orient=HORIZONTAL, command=self.createCanvas_Regler)
        self.regler.grid(row=3, sticky="nsew")

        self.regler.grid_forget()

    def createStatusbar(self):
        """Creates a Statusbar at the bottom of the app. It shows the name of the image"""
        self.label = StatusBar(self)
        self.label.grid(row=4, column=0, sticky="nsew")
        self.label.set("Image(s): ")

    def createVariables(self):
        """Variables and lists are stored here"""
        self.filename = StringVar()
        self.filename.set("No File Selected")

        self.filedirectory = StringVar()
        self.filedirectory.set("No Directory Selected")

        self.FilenameList = []

        self.FilenameObjectsList_Tk = []
        self.FilenameObjectsList_PIL = []

        self.resultList_ViewAsWindows = []

        self.statusVariable = StringVar()
        self.statusVariable.set('Status Bar')

        self.ImageNumberVar = IntVar()

    def getdirectory(self):
        fdir = askdirectory()
        if fdir:
            self.filedirectory.set(fdir)

    def createCanvas_Regler(self, ScaleValue):
        """Changes the image when the bar of the scale is moved"""
        self.img = self.FilenameObjectsList_Tk[self.ImageNumberVar.get()][int(ScaleValue) - 1]
        self.Canva.itemconfig(self.image_on_canvas, image=self.img)


"""The frames of the app"""


class StartPage(Frame):
    """The MainFrame. Navigation."""

    def __init__(self, parent):
        Frame.__init__(self, parent)

        """Make the main frame of StartPage stretchable"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        """Create the Layout"""
        self.createFrames()
        self.createButtons()

    def createFrames(self):
        self.frame1 = Frame(self)
        self.frame1.grid(row=0, column=0, sticky="ew")
        self.frame2 = Frame(self)
        self.frame2.grid(row=0, column=1, sticky="ew")

    def createButtons(self):
        button1 = Button(self.frame1, text="Filters", command=lambda: app.show_frame(Filters), width=20)
        button1.pack(fill=BOTH, pady=5, padx=5)
        button3 = Button(self.frame2, text="Create Windows", command=lambda: app.show_frame(ViewAsWindows), width=20)
        button3.pack(fill=BOTH, pady=5, padx=5)


class Filters(Frame):
    """A Frame for several filters"""

    def __init__(self, parent):
        Frame.__init__(self, parent)

        """Make the main frame stretchable"""
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        """The Radiobutton Variable"""
        self.rb = IntVar()
        self.rb.set(0)

        """Create the Layout"""
        self.createRadioButtons()
        self.createButtons()

    def createRadioButtons(self):
        rb1 = Radiobutton(self, text="Gaussian Filter", variable=self.rb, value=0)
        rb1.grid(row=0, column=0, sticky="w")

    def createButtons(self):
        button1 = Button(self, text="OK", width=20, command=self.ok)
        button1.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        button2 = Button(self, text="Back", width=20, command=lambda: app.show_frame(StartPage))
        button2.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    def ok(self):
        if self.rb.get() == 0:
            app.show_frame(GaussianFilter)


class ViewAsWindows(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.grid(sticky="nsew")

        """Making the frame ViewAsWindows strechable"""
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        """Variables in ViewAsWindows"""
        self.rb = IntVar()
        self.rb.set(1)

        self.checkVar = IntVar()
        self.checkVar2 = IntVar()

        """The body of the frame"""
        self.createFrames()
        self.createButtons()
        self.createEntries()
        self.createLabels()
        self.createRadiobuttons()
        self.createCheckbuttons()

    def createFrames(self):
        self.frame1 = LabelFrame(self, text="Mode", padx=5, pady=5)
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame2 = LabelFrame(self, text="Parameters", padx=5, pady=5)
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.frame2_1 = Frame(self.frame2)
        self.frame2_1.grid(row=0, column=1, pady=5, sticky="nsew")

        self.frame2_2 = Frame(self.frame2)
        self.frame2_2.grid(row=1, column=1, pady=5, sticky="nsew")

        self.frame2_3 = Frame(self.frame2)
        self.frame2_3.grid(row=2, column=1, pady=5, sticky="nsew")

        self.frame2_4 = Frame(self.frame2)
        self.frame2_4.grid(row=3, column=1, pady=5, sticky="nsew")

    def createRadiobuttons(self):
        rb1Gau = Radiobutton(self.frame1, text="2D", variable=self.rb, value=0, command=self.hide)
        rb2Gau = Radiobutton(self.frame1, text="3D", variable=self.rb, value=1, command=self.doNotHide)

        rb1Gau.pack(padx=20, anchor="w")
        rb2Gau.pack(padx=20, anchor="w")

    def createCheckbuttons(self):
        check1 = Checkbutton(self.frame2, text="Open folder when finished", variable=self.checkVar, onvalue=1,
                             offvalue=0)
        check1.grid(row=5, column=0, sticky="W")

        check2 = Checkbutton(self.frame2, text="Show Images when finished", variable=self.checkVar2, onvalue=1,
                             offvalue=0)
        check2.grid(row=6, column=0, sticky="W")

    def createLabels(self):
        label1 = Label(self.frame2, text="Window shape:")
        label1.grid(row=0, sticky="sw", padx=5, pady=5)
        label2 = Label(self.frame2, text="Step:")
        label2.grid(row=1, sticky="sw", padx=5, pady=5)
        label3 = Label(self.frame2, text="Color:")
        label3.grid(row=2, sticky="sw", padx=5, pady=5)
        label4 = Label(self.frame2, text="Checkbox shape:")
        label4.grid(row=3, sticky="sw", padx=5, pady=5)

        self.label1_1 = Label(self.frame2_1, text="Z")
        self.label1_1.grid(row=0, column=1)
        label1_2 = Label(self.frame2_1, text="Y")
        label1_2.grid(row=0, column=2)
        label1_3 = Label(self.frame2_1, text="X")
        label1_3.grid(row=0, column=3)

        self.label2_1 = Label(self.frame2_2, text="Z")
        self.label2_1.grid(row=0, column=1)
        label2_2 = Label(self.frame2_2, text="Y")
        label2_2.grid(row=0, column=2)
        label2_3 = Label(self.frame2_2, text="X")
        label2_3.grid(row=0, column=3)

        self.label4_1 = Label(self.frame2_4, text="Z")
        self.label4_1.grid(row=0, column=1)
        label4_2 = Label(self.frame2_4, text="Y")
        label4_2.grid(row=0, column=2)
        label4_3 = Label(self.frame2_4, text="X")
        label4_3.grid(row=0, column=3)

    def createButtons(self):
        button1 = Button(self, text="OK", command=self.ok, width=35)
        button1.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        button2 = Button(self, text="Back", width=35, command=lambda: app.show_frame(StartPage))
        button2.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    def createEntries(self):
        self.entry1_1 = Entry(self.frame2_1, width=3)
        self.entry1_1.grid(row=1, column=1, sticky="e")
        self.entry1_2 = Entry(self.frame2_1, width=3)
        self.entry1_2.grid(row=1, column=2, sticky="e")
        self.entry1_3 = Entry(self.frame2_1, width=3)
        self.entry1_3.grid(row=1, column=3, sticky="e")

        self.entry2_1 = Entry(self.frame2_2, width=3)
        self.entry2_1.grid(row=1, column=1, sticky="e")
        self.entry2_2 = Entry(self.frame2_2, width=3)
        self.entry2_2.grid(row=1, column=2, sticky="e")
        self.entry2_3 = Entry(self.frame2_2, width=3)
        self.entry2_3.grid(row=1, column=3, sticky="e")

        self.entry3 = Entry(self.frame2_3, width=10)
        self.entry3.grid(row=0, column=0, sticky="e")

        self.entry4_1 = Entry(self.frame2_4, width=3)
        self.entry4_1.grid(row=1, column=1, sticky="e")
        self.entry4_2 = Entry(self.frame2_4, width=3)
        self.entry4_2.grid(row=1, column=2, sticky="e")
        self.entry4_3 = Entry(self.frame2_4, width=3)
        self.entry4_3.grid(row=1, column=3, sticky="e")

    def hide(self):
        self.entry1_1.grid_forget()
        self.label1_1.grid_forget()

        self.entry2_1.grid_forget()
        self.label2_1.grid_forget()

        self.entry4_1.grid_forget()
        self.label4_1.grid_forget()

    def doNotHide(self):
        self.entry1_1 = Entry(self.frame2_1, width=3)
        self.entry1_1.grid(row=1, column=1, sticky="e")

        self.entry2_1 = Entry(self.frame2_2, width=3)
        self.entry2_1.grid(row=1, column=1, sticky="e")

        self.entry4_1 = Entry(self.frame2_4, width=3)
        self.entry4_1.grid(row=1, column=1, sticky="e")

        self.label1_1 = Label(self.frame2_1, text="Z")
        self.label1_1.grid(row=0, column=1)

        self.label2_1 = Label(self.frame2_2, text="Z")
        self.label2_1.grid(row=0, column=1)

        self.label4_1 = Label(self.frame2_4, text="Z")
        self.label4_1.grid(row=0, column=1)

    def ok(self):
        from utils import create_outline, create_Folder, create_CSV
        from Create_Windows import create_windows_slice, draw_windows

        app.getdirectory()
        """Resetting the results's list"""
        app.resultList_ViewAsWindows = []
        for j in app.FilenameList:
            app.filename.set(j)

            ImageBinary = imread(app.filename.get())

            if self.rb.get() == 0:
                filename = app.filename.get().split(".")[-2].split("/")[
                               -1] + "_(" + self.entry1_2.get() + "-" + self.entry1_3.get() + ")_" + self.entry2_1.get() + "_(" + self.entry4_2.get() + "-" + self.entry4_3.get() + ")_"
                window_shape = (int(self.entry1_2.get()), int(self.entry1_3.get()))
                step = (int(self.entry2_2.get()), int(self.entry2_3.get()))
                checkbox_shape = (int(self.entry4_2.get()), int(self.entry4_3.get()))
            if self.rb.get() == 1:
                filename = app.filename.get().split(".")[-2].split("/")[
                               -1] + "_(" + self.entry1_1.get() + "-" + self.entry1_2.get() + "-" + self.entry1_3.get() + ")_" + self.entry2_1.get()
                window_shape = (int(self.entry1_1.get()), int(self.entry1_2.get()), int(self.entry1_3.get()))
                step = (int(self.entry2_1.get()), int(self.entry2_2.get()), int(self.entry2_3.get()))
                checkbox_shape = (int(self.entry4_1.get()), int(self.entry4_2.get()), int(self.entry4_3.get()))

            color = int(self.entry3.get())

            save_dir = create_Folder(app.filedirectory.get(), filename)

            outline = create_outline(ImageBinary)
            outlineName = os.path.join(save_dir, filename + "_outline.tif")
            imsave(outlineName, outline)
            app.resultList_ViewAsWindows.append(outlineName)

            listCoords = create_windows_slice(outline, window_shape, step, checkbox_shape)

            if self.rb.get() == 0:
                create_CSV(save_dir, filename + "_coords", ['Y', 'X'],
                           [int(self.entry1_2.get()), int(self.entry1_3.get())], ";", listCoords)
            if self.rb.get() == 1:
                create_CSV(save_dir, filename + "_coords", ['Z', 'Y', 'X'],
                           [int(self.entry1_1.get()), int(self.entry1_2.get()), int(self.entry1_3.get())],
                           ";", listCoords)

            if self.rb.get() == 0:
                outlineWindows = draw_windows(listCoords, outline, window_shape, color)
            if self.rb.get() == 1:
                outlineWindows = draw_windows(listCoords, outline, window_shape, color)

            outlineWindowsName = os.path.join(save_dir, filename + "_windows.tif")
            imsave(outlineWindowsName, outlineWindows)
            app.resultList_ViewAsWindows.append(outlineWindowsName)

        messagebox.showinfo("", "Process done!")

        if sys.platform == 'win32' and self.checkVar.get() == 1:
            os.startfile(app.filedirectory.get())
        if self.checkVar2.get() == 1:
            self.resultWin = Resultwindow(app)


class GaussianFilter(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.createFrames()
        self.createButtons()
        self.createEntries()
        self.createLabels()
        self.rbGau = IntVar()
        self.rbGau.set(2)

        self.createRadiobuttons()

    def createFrames(self):
        self.frame1 = LabelFrame(self, text="Mode", padx=5, pady=5)
        self.frame1.grid(row=0, column=0, padx=10, pady=10)
        self.frame2 = LabelFrame(self, text="Parameters", padx=5, pady=5)
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def createRadiobuttons(self):
        rb1Gau = Radiobutton(self.frame1, text="reflect", variable=self.rbGau, value=0)
        rb2Gau = Radiobutton(self.frame1, text="constant", variable=self.rbGau, value=1)
        rb3Gau = Radiobutton(self.frame1, text="nearest (default)", variable=self.rbGau, value=2)
        rb4Gau = Radiobutton(self.frame1, text="mirror", variable=self.rbGau, value=3)
        rb5Gau = Radiobutton(self.frame1, text="wrap", variable=self.rbGau, value=4)

        rb1Gau.pack(padx=20, anchor="w")
        rb2Gau.pack(padx=20, anchor="w")
        rb3Gau.pack(padx=20, anchor="w")
        rb4Gau.pack(padx=20, anchor="w")
        rb5Gau.pack(padx=20, anchor="w")

    def createLabels(self):
        Label1 = Label(self.frame2, text="Sigma: ")
        Label1.grid(row=0, column=0, sticky="w")

    def createButtons(self):
        button1 = Button(self, text="OK", command=self.ok, width=20)
        button1.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        button2 = Button(self, text="Back", width=20, command=lambda: app.show_frame(Filters))
        button2.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    def createEntries(self):
        self.entry1 = Entry(self.frame2, width=5)
        self.entry1.grid(row=0, column=1)

    def ok(self):
        app.getdirectory()
        for j in app.FilenameList:
            app.filename.set(j)
            array = imread(app.filename.get())

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

            newArray = gaussian(array, sigma=int(self.entry1.get()), preserve_range=True, mode=gaussianMode)

            completeFilename = app.filename.get()
            filenameWithoutEnding = completeFilename.split(".")[-2]
            filename = filenameWithoutEnding.split("/")[-1]
            filenameExtended = filename + "_gaussianFilter_sigma=" + self.entry1.get() + "_mode=" + gaussianMode + ".tif"
            savedir_filename = os.path.join(app.filedirectory.get(), filenameExtended)
            imsave(savedir_filename, np.uint8(newArray))
            app.resultList_ViewAsWindows.append(savedir_filename)
        messagebox.showinfo("", "Process done with Sigma %d" % (int(self.entry1.get())))

        self.resultWin = Resultwindow(app)


"""The Toplevel Windows"""


class Resultwindow(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        """Make the window stretchable"""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        """Create the Layout"""
        self.createVariables()
        self.createScale()
        self.createStatusbar()

        """Create Imageslists"""
        for i in range(0, len(parent.resultList_ViewAsWindows)):
            self.Filename = parent.resultList_ViewAsWindows[i]
            self.FilenameList.append(self.Filename)
        self.size = 800, 800
        self.createImageLists(self.size, self.FilenameList)

        """Create Canvas"""
        self.createCanvas()
        self.updateCanvasButtons()

    def createVariables(self):

        self.FilenameList = []
        self.FilenameObjectsList_Tk = []
        self.FilenameObjectsList_PIL = []

        self.statusVariable = StringVar()
        self.statusVariable.set('Status Bar')

        self.ImageNumberVar = IntVar()

        """Create Canvas"""

    def createImageLists(self, size, list):
        for element in list:
            self.imgArray = imread(element)
            """Check the dimensions and mode of each image"""
            if self.imgArray.ndim == 2 or Image.open(element).mode == 'RGB':
                self.img = Image.open(element)
                self.img.thumbnail(size, Image.ANTIALIAS)
                self.FilenameObjectsList_PIL.append(self.img)
                self.imageTk = ImageTk.PhotoImage(self.img)
                self.FilenameObjectsList_Tk.append(self.imageTk)
            if self.imgArray.ndim == 3 and Image.open(element).mode != 'RGB':
                self.Slices_List_PIL = []
                for Slice in range(0, self.imgArray.shape[0]):
                    self.img = Image.fromarray(np.uint8(self.imgArray[Slice, :, :]))
                    self.img.thumbnail(size, Image.ANTIALIAS)
                    self.Slices_List_PIL.append(self.img)
                self.Slices_List_Tk = [ImageTk.PhotoImage(i) for i in self.Slices_List_PIL]

                self.FilenameObjectsList_PIL.append(self.Slices_List_PIL)
                self.FilenameObjectsList_Tk.append(self.Slices_List_Tk)

    def changeImage(self, x):
        self.ImageNumberVar.set(x)

        if type(self.FilenameObjectsList_Tk[self.ImageNumberVar.get()]) == list:

            self.Canva.itemconfig(self.image_on_canvas,
                                  image=self.FilenameObjectsList_Tk[self.ImageNumberVar.get()][0])
            self.Canva.config(height=self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[1],
                              width=self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[0])

            self.butt1_window = self.Canva.create_window(
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[0] - 80,
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[1] - 25,
                anchor=NW,
                window=self.butt1)
            self.butt2_window = self.Canva.create_window(
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[0] - 165,
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()][0].size[1] - 25, anchor=NW,
                window=self.butt2)
            self.updateScale(x)


        else:
            self.Canva.itemconfig(self.image_on_canvas,
                                  image=self.FilenameObjectsList_Tk[self.ImageNumberVar.get()])
            self.Canva.config(height=self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[1],
                              width=self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[0])

            self.butt1_window = self.Canva.create_window(
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[0] - 80,
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[1] - 25,
                anchor=NW,
                window=self.butt1)
            self.butt2_window = self.Canva.create_window(
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[0] - 165,
                self.FilenameObjectsList_PIL[self.ImageNumberVar.get()].size[1] - 25, anchor=NW,
                window=self.butt2)
            try:
                self.regler.grid_forget()
            except AttributeError:
                pass

        """Update"""
        self.updateCanvasButtons()
        self.updateStatusbar()

    def updateStatusbar(self):
        self.label.set("Image(s): " + self.FilenameList[self.ImageNumberVar.get()].split("/")[-1].split("\\")[-1])

    def updateScale(self, y):
        try:
            self.regler.grid_forget()
        except AttributeError:
            pass
        self.regler.grid(row=3, sticky="nsew")
        self.regler['to'] = len(self.FilenameObjectsList_PIL[y])

    def updateCanvasButtons(self):
        if self.ImageNumberVar.get() > 0 and self.ImageNumberVar.get() != len(self.FilenameList) - 1:
            self.butt1['state'] = 'normal'
            self.butt2['state'] = 'normal'
        if self.ImageNumberVar.get() == 0 and len(self.FilenameList) - 1 != 0:
            self.butt1['state'] = 'normal'
            self.butt2['state'] = 'disabled'
        if self.ImageNumberVar.get() == len(self.FilenameList) - 1:
            self.butt1['state'] = 'disabled'
            self.butt2['state'] = 'normal'
        if len(self.FilenameList) - 1 == 0:
            self.butt1['state'] = 'disabled'
            self.butt2['state'] = 'disabled'

    def createCanvas(self):
        if type(self.FilenameObjectsList_PIL[0]) == list:
            self.Canva = Canvas(self, width=self.FilenameObjectsList_PIL[0][0].size[0],
                                height=self.FilenameObjectsList_PIL[0][0].size[1])
            self.Canva.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            self.image_on_canvas = self.Canva.create_image(0 + 2, 0 + 2, image=self.FilenameObjectsList_Tk[0][0],
                                                           anchor=NW)

            self.ImageNumberVar.set(self.FilenameObjectsList_Tk.index(self.FilenameObjectsList_Tk[0]))
            self.Canva.config(height=self.FilenameObjectsList_PIL[0][0].size[1],
                              width=self.FilenameObjectsList_PIL[0][0].size[0])

            """Create Buttons for Canvas"""
            self.butt1 = Button(self, text="Next", command=self.nextButtonCanvas, width=10, height=1)
            self.butt1_window = self.Canva.create_window(self.FilenameObjectsList_PIL[0][0].size[0] - 80,
                                                         self.FilenameObjectsList_PIL[0][0].size[1] - 25, anchor=NW,
                                                         window=self.butt1)
            self.butt2 = Button(self, text="Back", command=self.backButtonCanvas, width=10, height=1)
            self.butt2_window = self.Canva.create_window(self.FilenameObjectsList_PIL[0][0].size[0] - 165,
                                                         self.FilenameObjectsList_PIL[0][0].size[1] - 25, anchor=NW,
                                                         window=self.butt2)

            self.updateScale(self.ImageNumberVar.get())


        else:
            self.Canva = Canvas(self, width=self.FilenameObjectsList_PIL[0].size[0],
                                height=self.FilenameObjectsList_PIL[0].size[1])
            self.Canva.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            self.image_on_canvas = self.Canva.create_image(0 + 2, 0 + 2, image=self.FilenameObjectsList_Tk[0],
                                                           anchor=NW)

            self.ImageNumberVar.set(self.FilenameObjectsList_Tk.index(self.FilenameObjectsList_Tk[0]))
            self.Canva.config(height=self.FilenameObjectsList_PIL[0].size[1],
                              width=self.FilenameObjectsList_PIL[0].size[0])

            """Create Buttons for Canvas"""
            self.butt1 = Button(self, text="Next", command=self.nextButtonCanvas, width=10, height=1)
            self.butt1_window = self.Canva.create_window(self.FilenameObjectsList_PIL[0].size[0] - 80,
                                                         self.FilenameObjectsList_PIL[0].size[1] - 25, anchor=NW,
                                                         window=self.butt1)
            self.butt2 = Button(self, text="Back", command=self.backButtonCanvas, width=10, height=1)
            self.butt2_window = self.Canva.create_window(self.FilenameObjectsList_PIL[0].size[0] - 165,
                                                         self.FilenameObjectsList_PIL[0].size[1] - 25, anchor=NW,
                                                         window=self.butt2)

        """Update"""
        self.updateStatusbar()

    def nextButtonCanvas(self):
        self.changeImage(self.ImageNumberVar.get() + 1)
        self.updateCanvasButtons()

    def backButtonCanvas(self):
        self.changeImage(self.ImageNumberVar.get() - 1)
        self.updateCanvasButtons()

    def createScale(self):
        """Creates and shows a scale if the opened Image is a stack"""
        self.regler = Scale(self, from_=1, to=100, orient=HORIZONTAL, command=self.createCanvas_Regler)
        self.regler.grid(row=3, sticky="nsew")

        self.regler.grid_forget()

    def createStatusbar(self):
        """Creates a Statusbar at the bottom of the app. It shows the name of the image"""
        self.label = StatusBar(self)
        self.label.grid(row=4, column=0, sticky="nsew")
        self.label.set("Image(s): ")

    def createCanvas_Regler(self, ScaleValue):
        """Changes the image when the bar of the scale is moved"""
        self.img = self.FilenameObjectsList_Tk[self.ImageNumberVar.get()][int(ScaleValue) - 1]
        self.Canva.itemconfig(self.image_on_canvas, image=self.img)


"""Other Classes"""


class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


if __name__ == "__main__":
    app = App()
    app.mainloop()
