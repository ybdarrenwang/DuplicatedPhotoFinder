import re
import Tkinter, tkFont, tkFileDialog, tkMessageBox
from canvas import PhotoCanvas
from config import *
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
        batch_photo_frame: to display the thumbs of all duplicated photos
        selected_photo_frame: to display the selected photo
        photo_crawler: a generator that yields a list of duplicated photos
        cached_cv: a list of canvases; cached_cv[0] display the selected photo, others are photo thumbs.
        """
        if len(photo_crawler)==0:
            tkMessageBox.showinfo("Warning", "Please choose a folder.")
            return
        if cached_cv: # delete canvases of previous batch
            for cv in cached_cv:
                cv.destroy()
            del cached_cv[:]
        try:
            # fetch next batch
            copies = photo_crawler[-1].next()
            # show the first photo in selected_photo_frame
            cached_cv.append(PhotoCanvas(copies[0], selected_photo_frame, DISPLAY_HEIGHT))
            # show duplicated photo thumbs in batch_photo_frame
            for idx,cp in enumerate(copies):
                cached_cv.append(PhotoCanvas(cp, batch_photo_frame, THUMB_HEIGHT, cached_cv[0]))
            # copy pointers of all thumbs to each of them, so they can remove others' highlights when needed
            for cv in cached_cv[1:]:
                cv.setCompetingCanvases(cached_cv[1:])
            # highlight the first picture
            cached_cv[1].highlight()
            root.update_idletasks()
        except StopIteration:
            tkMessageBox.showinfo("Warning", "No more duplicated photos found.")
