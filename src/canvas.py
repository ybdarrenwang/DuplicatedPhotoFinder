import Tkinter, Tkconstants, tkMessageBox
from PIL import Image, ImageTk

class PhotoCanvas(Tkinter.Canvas):
    """ Display photo object, interact with mouse click, and control other
    canvases when necessary.

    Under current setup, 2 kinds of PhotoCanvas objects would be created:
    1. display canvas: large canvas displaying selected image;
    2. thumb canvas: small canvas displaying duplicated images.

    # Member objects
        photo: An Photo object (c.f. database.py).
        info_label: Texts to display when selected.
        max_height: Maximum height of display.
        max_width: Maximum width of display.
        cache_tkinter_canvas: Cache of Tkinter canvas image.
        cache_python_image: Cache of Python image object.
        default_color: Boarder color when not selected.
        thumb_canvases: Other thumb canvases except self.
        display_canvas: Large canvas for displaying image upon click.
        is_selected: True when this canvas is selected by mouse click; false
                     otherwise.
    """
    def __init__(self, photo, parent, max_height=None, max_width=None, display_canvas=None, info_label=None):
        Tkinter.Canvas.__init__(self, parent, width=max_width, height=max_height, highlightthickness=2, relief='ridge', background='white')
        self.photo = photo
        self.info_label = info_label
        self.max_height = max_height
        self.max_width = max_width
        self.cache_tkinter_canvas = [None]
        self.cache_python_image = [None]
        self.default_color = self.cget("bg")
        self.thumb_canvases = []
        self.display_canvas = display_canvas
        if self.display_canvas==None: # display canvas: resize upon main window resize
            self.bind("<Configure>", self.on_resize)
            self.pack(fill=Tkinter.BOTH, expand=True)
        else: # thumb canvases: highlight upon click
            self.bind("<Button-1>", lambda event: self.on_click())
            self.pack(side=Tkinter.LEFT)
        self.is_selected = False
        self.loadImage(self.photo)

    def on_click(self):
        """ Upon clicked:
        1. remove highlights of other thumbs;
        2. highlight self by setting red boarder color;
        3. update desplayed photo info
        4. update displayed large image in display_canvas
        """
        for cv in self.thumb_canvases:
            cv.configure(highlightbackground=cv.default_color, highlightcolor=cv.default_color)
            cv.is_selected = False
        self.configure(highlightbackground="red", highlightcolor="red")
        self.is_selected = True
        self.info_label.configure(text=self.photo.info)
        if self.display_canvas!=None:
            self.display_canvas.loadImage(self.photo)

    def on_resize(self, event):
        self.max_height = event.height
        self.max_width = event.width
        self.loadImage(self.photo)

    def loadImage(self, photo):
        # resize image if necessary
        height, width, channel = photo.shape
        ratio = 1
        if self.max_height!=None or self.max_width!=None:
            if self.max_height is None:
                ratio = float(width)/self.max_width
            elif self.max_width is None:
                ratio = float(height)/self.max_height
            else:
                ratio = max(float(height)/self.max_height, float(width)/self.max_width)
        self.width = int(float(width)/ratio)
        self.height = int(float(height)/ratio)
        self.config(width=self.width, height=self.height)
        # load image
        tmp = Image.open(photo.path).resize((self.width, self.height), Image.ANTIALIAS)
        self.cache_python_image[0] = ImageTk.PhotoImage(tmp)
        if self.cache_tkinter_canvas[0]==None:
            self.cache_tkinter_canvas[0] = self.create_image(0, 0, image = self.cache_python_image[0], anchor='nw')
        else:
            self.itemconfig(self.cache_tkinter_canvas[0], image = self.cache_python_image[0])

    def setThumbCanvases(self, thumb_canvases):
        self.thumb_canvases = thumb_canvases
