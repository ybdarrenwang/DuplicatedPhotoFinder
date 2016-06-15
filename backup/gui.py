import Tkinter, Tkconstants
from PIL import Image, ImageTk
import gui_methods

class Canvas(object):
    def __init__(self, parent, w, h):
        print "__init__"
        self.width = w
        self.height = h
        self.canvas = Tkinter.Canvas(parent, width=w, height=h)
        self.canvas.pack(side=Tkinter.LEFT)
        self.img = [None]
        self.thumb = [None]

    def loadImages(self, image):
        print "load "+image
        tmp = Image.open(image).resize((self.width, self.height), Image.ANTIALIAS)
        self.thumb[0] = ImageTk.PhotoImage(tmp)
        if self.img[0]==None:
            self.img[0] = self.canvas.create_image(0, 0, image = self.thumb[0], anchor='nw')
        else:
            self.canvas.itemconfig(self.img[0], image = self.thumb[0])

class Button(object):
    def __init__(self, bt, options):
        self.bt = bt
        self.options = options

    @classmethod
    def loadFolder(cls, parent, frame):
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = parent
        #options['title'] = 'This is a title'
        bt = Tkinter.Button(parent, text='Load folder', command=lambda:gui_methods.askdirectory(options, parent, frame))
        bt.pack(side=Tkinter.BOTTOM)
        return cls(bt, options)
