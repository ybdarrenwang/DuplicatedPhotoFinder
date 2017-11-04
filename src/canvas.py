import Tkinter, Tkconstants, tkMessageBox
from PIL import Image, ImageTk

class PhotoCanvas(Tkinter.Canvas):
    """ Display photo object, interact with mouse click, and control other
    canvases when necessary.

    # Member objects
        photo: An Photo object (c.f. database.py).
        info_label: Texts to display when selected.
        max_height: Maximum height of display.
        max_width: Maximum width of display.
        img: Cache of Tkinter canvas image.
        thumb: Cache of Python image object.
        default_color: Boarder color when not selected.
        competing_canvas: Upon clicked, remove highlights on these canvases.
        is_selected: True when this canvas is selected by mouse click; false
                     otherwise.
        extraCanvas4Display: An additional canvas object for displaying image upon click
    """
    def __init__(self, photo, parent, max_height=None, max_width=None, extraCanvas4Display=None, info_label=None):
        """ extraCanvas4Display: upon clicked, display image on this canvas as well. """
        # prepare for file info display
        self.photo = photo
        self.info_label = info_label
        self.max_height = max_height
        self.max_width = max_width
        # create canvas, cache and display image
        Tkinter.Canvas.__init__(self, parent, width=max_width, height=max_height, highlightthickness=2, relief='ridge', background='white')
        self.img = [None]
        self.thumb = [None]
        self.loadImages(self.photo)
        # prepare for highlight upon click
        self.default_color = self.cget("bg")
        self.competing_canvas = []
        self.extraCanvas4Display = extraCanvas4Display
        if self.extraCanvas4Display==None:
            self.pack()
        else:
            self.bind("<Button-1>", lambda event: self.highlight())
            self.pack(side=Tkinter.LEFT)
        self.is_selected = False

    def setCompetingCanvases(self, competingCanvasList):
        self.competing_canvas = competingCanvasList

    def highlight(self):
        """ extraCanvas4Display: upon clicked, display image on this canvas as well. """
        for cv in self.competing_canvas:
            cv.configure(highlightbackground=cv.default_color, highlightcolor=cv.default_color)
            cv.is_selected = False
        self.configure(highlightbackground="red", highlightcolor="red")
        self.is_selected = True
        self.info_label.configure(text=self.photo.info)
        if self.extraCanvas4Display!=None:
            self.extraCanvas4Display.loadImages(self.photo)

    def loadImages(self, photo):
        # resize canvas if necessary
        height, width, channel = photo.shape
        ratio = 1
        if self.max_height!=None or self.max_width!=None:
            if self.max_height==None:
                ratio = float(width)/self.max_width
            elif self.max_width==None:
                ratio = float(height)/self.max_height
            else:
                ratio = max(float(height)/self.max_height, float(width)/self.max_width)
        self.width = int(float(width)/ratio)
        self.height = int(float(height)/ratio)
        self.config(width=self.width, height=self.height)
        # load image
        tmp = Image.open(photo.path).resize((self.width, self.height), Image.ANTIALIAS)
        self.thumb[0] = ImageTk.PhotoImage(tmp)
        if self.img[0]==None:
            self.img[0] = self.create_image(0, 0, image = self.thumb[0], anchor='nw')
        else:
            self.itemconfig(self.img[0], image = self.thumb[0])
