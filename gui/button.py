import Tkinter, tkFont
import tkFileDialog, tkMessageBox
from canvas import Canvas
from config import *
import re
import util

class OpenFolderButton(Tkinter.Button):
    def __init__(self, parent, frame):
        self.crawler = []
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = parent
        ft = tkFont.Font(family=FONT_FAMILY, size=FONT_SIZE)
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Open folder', font=ft, command=lambda:self.askdirectory(self.crawler, options, parent, frame))
        self.pack(side=Tkinter.LEFT)
    @staticmethod
    def askdirectory(crawler, options, root, frame):
        path = re.escape(tkFileDialog.askdirectory(**options))
        if path:
            del crawler[:]
            crawler.append(util.duplicatePhotoCrawler(path))

class NextBatchButton(Tkinter.Button):
    def __init__(self, parent, batch_photo_frame, selected_photo_frame, bt):
        self.cachedPics = []
        ft = tkFont.Font(family=FONT_FAMILY, size=FONT_SIZE)
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Find duplicates', font=ft, command=lambda:self.getNextDuplicatedBatch(parent, batch_photo_frame, selected_photo_frame, bt, self.cachedPics))
        self.pack(side=Tkinter.RIGHT)
    @staticmethod
    def getNextDuplicatedBatch(root, batch_photo_frame, selected_photo_frame, bt, cache):
        if cache:
            for cv in cache:
                cv.destroy()
            del cache[:]
        if len(bt.crawler)==0:
            tkMessageBox.showinfo("Warning", "Please choose a folder.")
            return
        try:
            copies = bt.crawler[-1].next()
            # show the first photo in selected_photo_frame
            height, width, channel = copies[0]["shape"]
            ratio = float(height)/DISPLAY_HEIGHT
            cache.append(Canvas(selected_photo_frame, int(width/ratio), int(height/ratio)))
            cache[0].loadImages(copies[0]["path"])
            # show duplicated photo thumbs in batch_photo_frame
            for idx,cp in enumerate(copies):
                height, width, channel = cp["shape"]
                ratio = float(height)/THUMB_HEIGHT
                cache.append(Canvas(batch_photo_frame, int(width/ratio), int(height/ratio), cache[0], cp["path"]))
                cache[-1].loadImages(cp["path"])
            root.update_idletasks()
        except StopIteration:
            tkMessageBox.showinfo("Warning", "No more duplicated photos found.")
