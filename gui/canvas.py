import Tkinter, Tkconstants, tkMessageBox
from PIL import Image, ImageTk

class Canvas(Tkinter.Canvas):
    def __init__(self, parent, w, h, canvas4display=None, img_path=None):
        self.width = w
        self.height = h
        Tkinter.Canvas.__init__(self, parent, width=w, height=h)
        if canvas4display==None:
            self.pack()
        else:
            self.bind("<Button-1>", lambda event, cv=canvas4display, img=img_path: self.showcaseImage(cv, img))
            self.pack(side=Tkinter.LEFT)
        self.img = [None]
        self.thumb = [None]

    def showcaseImage(self, cv4display, img_path):
        cv4display.loadImages(img_path)

    def loadImages(self, image):
        tmp = Image.open(image).resize((self.width, self.height), Image.ANTIALIAS)
        self.thumb[0] = ImageTk.PhotoImage(tmp)
        if self.img[0]==None:
            self.img[0] = self.create_image(0, 0, image = self.thumb[0], anchor='nw')
        else:
            itemconfig(self.img[0], image = self.thumb[0])
