import Tkinter, Tkconstants, tkMessageBox
from PIL import Image, ImageTk

class PhotoCanvas(Tkinter.Canvas):
    """
    extraCanvas4Display: upon clicked, display image on this canvas as well
    competingCanvasList: upon clicked, remove highlights on these canvases
    Note: will resize the image based on display_height
    """
    def __init__(self, image, parent, display_height, extraCanvas4Display=None):
        # configure display
        height, width, channel = image["shape"]
        self.width = int(float(width)/height*display_height)
        self.height = display_height
        self.path = image["path"]
        Tkinter.Canvas.__init__(self, parent, width=self.width, height=self.height, highlightthickness=2, relief='ridge')
        # display image
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
        if extraCanvas4Display!=None:
            extraCanvas4Display.loadImages(self.path)

    def loadImages(self, image):
        tmp = Image.open(image).resize((self.width, self.height), Image.ANTIALIAS)
        self.thumb[0] = ImageTk.PhotoImage(tmp)
        if self.img[0]==None:
            self.img[0] = self.create_image(0, 0, image = self.thumb[0], anchor='nw')
        else:
            self.itemconfig(self.img[0], image = self.thumb[0])
