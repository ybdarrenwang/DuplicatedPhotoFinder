import Tkinter, Tkconstants, tkMessageBox
from PIL import Image, ImageTk

class PhotoCanvas(Tkinter.Canvas):
    def __init__(self, image, parent, display_height, extraCanvas4Display=None):
        """
        Note: will resize the image based on display_height
        """
        height, width, channel = image["shape"]
        self.width = int(float(width)/height*display_height)
        self.height = display_height
        self.path = image["path"]
        Tkinter.Canvas.__init__(self, parent, width=self.width, height=self.height)
        if extraCanvas4Display==None:
            self.pack()
        else:
            self.bind("<Button-1>", lambda event: extraCanvas4Display.loadImages(self.path))
            self.pack(side=Tkinter.LEFT)
        self.img = [None] # cache of Tkinter canvas image
        self.thumb = [None] # cache of Python image object
        self.loadImages(self.path)

    def loadImages(self, image):
        tmp = Image.open(image).resize((self.width, self.height), Image.ANTIALIAS)
        self.thumb[0] = ImageTk.PhotoImage(tmp)
        if self.img[0]==None:
            self.img[0] = self.create_image(0, 0, image = self.thumb[0], anchor='nw')
        else:
            self.itemconfig(self.img[0], image = self.thumb[0])
