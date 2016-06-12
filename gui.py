import re
import Tkinter, Tkconstants, tkFileDialog
from PIL import Image, ImageTk
from util import *

class Canvas(object):
    def __init__(self, root):
        self.canvas1 = Tkinter.Canvas(root, width=250, height=250)
        self.canvas1.pack(side=Tkinter.LEFT)
        self.canvas2 = Tkinter.Canvas(root, width=250, height=250)
        self.canvas2.pack(side=Tkinter.LEFT)
        self.img = [None, None]
        self.thumb = [None, None]

    def loadImages(self, photo1, photo2):
        print photo1
        print photo2
        tmp = Image.open(photo1).resize((250, 250), Image.ANTIALIAS)
        self.thumb[0] = ImageTk.PhotoImage(tmp)
        if self.img[0]==None:
            self.img[0] = self.canvas1.create_image(0, 0, image = self.thumb[0], anchor='nw')
        else:
            self.canvas1.itemconfig(self.img[0], image = self.thumb[0])
        tmp = Image.open(photo2).resize((250, 250), Image.ANTIALIAS)
        self.thumb[1] = ImageTk.PhotoImage(tmp)
        if self.img[1]==None:
            self.img[1] = self.canvas2.create_image(0, 0, image = self.thumb[1], anchor='nw')
        else:
            self.canvas2.itemconfig(self.img[1], image = self.thumb[1])

class Button(object):
    def __init__(self, root, canvas):
        self.bt = Tkinter.Button(root, text='Open folder', command=self.askdirectory)
        self.bt.pack(side=Tkinter.BOTTOM)
        self.options = {}
        self.options['initialdir'] = 'C:\\'
        self.options['mustexist'] = False
        self.options['parent'] = root
        self.options['title'] = 'This is a title'
        self.root = root
        self.canvas = canvas

    def askdirectory(self):
        path = re.escape(tkFileDialog.askdirectory(**self.options))
        crawler = photoCrawler(path)
        findDuplicatePair(self.root, self.canvas, crawler)
