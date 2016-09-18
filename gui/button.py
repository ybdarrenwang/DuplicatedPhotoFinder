import Tkinter, tkFont
import tkFileDialog, tkMessageBox
from canvas import Canvas
from config import *
import re
import util

class OpenFolderButton(Tkinter.Button):
    """
    Note: this class creates and owns the photo crawler while opening the
    target folder, which will be passed to other functions for crawling.
    """
    def __init__(self, parent, frame):
        self.photo_crawler = []
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = parent
        ft = tkFont.Font(family=FONT_FAMILY, size=FONT_SIZE)
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Open folder', font=ft, command=lambda:self.askdirectory(self.photo_crawler, options, parent, frame))
        self.pack(side=Tkinter.LEFT)

    @staticmethod
    def askdirectory(photo_crawler, options, root, frame):
        path = re.escape(tkFileDialog.askdirectory(**options))
        if path:
            del photo_crawler[:]
            photo_crawler.append(util.duplicatePhotoCrawler(path))


class NextBatchButton(Tkinter.Button):
    def __init__(self, parent, batch_photo_frame, selected_photo_frame, photo_crawler):
        self.cached_canvases = []
        ft = tkFont.Font(family=FONT_FAMILY, size=FONT_SIZE)
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Find duplicates', font=ft, command=lambda:self.getNextDuplicatedBatch(parent, batch_photo_frame, selected_photo_frame, photo_crawler, self.cached_canvases))
        self.pack(side=Tkinter.RIGHT)

    @staticmethod
    def getNextDuplicatedBatch(root, batch_photo_frame, selected_photo_frame, photo_crawler, cached_cv):
        """
        cached_cv: a list of canvases; cached_cv[0] display the selected photo, others are photo thumbs.
        """
        if len(photo_crawler)==0:
            tkMessageBox.showinfo("Warning", "Please choose a folder.")
            return
        if cached_cv: # delete canvases of previous batch
            for cv in cached_cv:
                cv.destroy()
            del cached_cv[:]
        try: # fetch next batch
            copies = photo_crawler[-1].next()
            # show the first photo in selected_photo_frame
            height, width, channel = copies[0]["shape"]
            ratio = float(height)/DISPLAY_HEIGHT
            cached_cv.append(Canvas(selected_photo_frame, int(width/ratio), int(height/ratio)))
            cached_cv[0].loadImages(copies[0]["path"])
            # show duplicated photo thumbs in batch_photo_frame
            for idx,cp in enumerate(copies):
                height, width, channel = cp["shape"]
                ratio = float(height)/THUMB_HEIGHT
                cached_cv.append(Canvas(batch_photo_frame, int(width/ratio), int(height/ratio), cached_cv[0], cp["path"]))
                cached_cv[-1].loadImages(cp["path"])
            root.update_idletasks()
        except StopIteration:
            tkMessageBox.showinfo("Warning", "No more duplicated photos found.")
