import Tkinter, Tkconstants, tkMessageBox
from PIL import Image, ImageTk

class Canvas(object):
    def __init__(self, parent, w, h, canvas4display=None, img_path=None):
        self.width = w
        self.height = h
        self.canvas = Tkinter.Canvas(parent, width=w, height=h)
        if canvas4display==None:
            self.canvas.pack()
        else:
            self.canvas.bind("<Button-1>", lambda event, cv=canvas4display, img=img_path: self.showcaseImage(cv, img))
            self.canvas.pack(side=Tkinter.LEFT)
        self.img = [None]
        self.thumb = [None]

    def showcaseImage(self, cv4display, img_path):
        cv4display.loadImages(img_path)

    def loadImages(self, image):
        tmp = Image.open(image).resize((self.width, self.height), Image.ANTIALIAS)
        self.thumb[0] = ImageTk.PhotoImage(tmp)
        if self.img[0]==None:
            self.img[0] = self.canvas.create_image(0, 0, image = self.thumb[0], anchor='nw')
        else:
            self.canvas.itemconfig(self.img[0], image = self.thumb[0])

    def destroy(self):
        self.canvas.destroy()
