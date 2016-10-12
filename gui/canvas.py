import os, datetime
import Tkinter, Tkconstants, tkMessageBox
from PIL import Image, ImageTk

class PhotoCanvas(Tkinter.Canvas):
    """
    extraCanvas4Display: upon clicked, display image on this canvas as well
    competingCanvasList: upon clicked, remove highlights on these canvases
    Note: will resize the image based on display_height
    """
    def __init__(self, image, parent, max_height=None, max_width=None, extraCanvas4Display=None, info_label=None):
        # resize picture if necessary
        height, width, channel = image["shape"]
        ratio = 1
        if max_height!=None or max_width!=None:
            if max_height==None:
                ratio = float(width)/max_width
            elif max_width==None:
                ratio = float(height)/max_height
            else:
                ratio = max(float(height)/max_height, float(width)/max_width)
        self.width = int(float(width)/ratio)
        self.height = int(float(height)/ratio)
        # prepare for file info display
        self.path = image["path"]
        self.info_label = info_label
        # create canvas and display image
        Tkinter.Canvas.__init__(self, parent, width=self.width, height=self.height, highlightthickness=2, relief='ridge', background='white')
        self.img = [None] # cache of Tkinter canvas image
        self.thumb = [None] # cache of Python image object
        self.loadImages(self.path)
        # prepare for highlight upon click
        self.default_color = self.cget("bg")
        self.competing_canvas = []
        if extraCanvas4Display==None:
            self.pack()
        else:
            self.bind("<Button-1>", lambda event: self.highlight(extraCanvas4Display))
            self.pack(side=Tkinter.LEFT)

    def setCompetingCanvases(self, competingCanvasList):
        self.competing_canvas = competingCanvasList

    def highlight(self, extraCanvas4Display=None):
        for cv in self.competing_canvas:
            cv.configure(highlightbackground=cv.default_color, highlightcolor=cv.default_color)
        self.configure(highlightbackground="red", highlightcolor="red")
        info = '\n'.join(["File name:", self.path.split('/')[-1],'',
                          "File size (kB):", str(round(float(os.stat(self.path).st_size)/1000, 1)),'',
                          "Last modified:", str(datetime.datetime.fromtimestamp(os.stat(self.path).st_mtime))])
        self.info_label.configure(text=info)
        if extraCanvas4Display!=None:
            extraCanvas4Display.loadImages(self.path)

    def loadImages(self, image):
        tmp = Image.open(image).resize((self.width, self.height), Image.ANTIALIAS)
        self.thumb[0] = ImageTk.PhotoImage(tmp)
        if self.img[0]==None:
            self.img[0] = self.create_image(0, 0, image = self.thumb[0], anchor='nw')
        else:
            self.itemconfig(self.img[0], image = self.thumb[0])
