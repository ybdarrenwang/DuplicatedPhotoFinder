import Tkinter, Tkconstants
from PIL import Image, ImageTk

class Canvas(object):
    def __init__(self, parent, w, h, isCentered=False):
        self.width = w
        self.height = h
        self.canvas = Tkinter.Canvas(parent, width=w, height=h)
        if isCentered:
            self.canvas.pack()
        else:
            #self.canvas.bind("<Button-1>", callback)
            self.canvas.pack(side=Tkinter.LEFT)
        self.img = [None]
        self.thumb = [None]

    def loadImages(self, image):
        tmp = Image.open(image).resize((self.width, self.height), Image.ANTIALIAS)
        self.thumb[0] = ImageTk.PhotoImage(tmp)
        if self.img[0]==None:
            self.img[0] = self.canvas.create_image(0, 0, image = self.thumb[0], anchor='nw')
        else:
            self.canvas.itemconfig(self.img[0], image = self.thumb[0])

    def destroy(self):
        self.canvas.destroy()
