import re
import Tkinter, tkFont, tkFileDialog, tkMessageBox
from canvas import PhotoCanvas
from config import *
import util

class CloseWindowButton(Tkinter.Button):
    def __init__(self, parent):
        self.root = parent
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Done', font=tkFont.Font(family=FONT_FAMILY, size=DIALOG_FONT_SIZE), command=self.close)
        self.pack(side=Tkinter.RIGHT, padx=5, pady=5)

    def close(self):
        self.root.destroy()


class ConfigButton(Tkinter.Button):
    """
    This class owns configuration for photo similarity calculation, which will
    be passed to the photo cralwer.
    """
    def __init__(self, parent, r, c):
        self.config = {}
        self.config['dist'] = Tkinter.StringVar()
        self.config['dist'].set('l1')
        self.config['th_l1'] = Tkinter.IntVar()
        self.config['th_l1'].set(30)
        self.config['th_l2'] = Tkinter.IntVar()
        self.config['th_l2'].set(50)
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Preference...', font=tkFont.Font(family=FONT_FAMILY, size=BUTTON_FONT_SIZE), command=self.openConfig)
        self.grid(row=r, column=c, padx=5, pady=5)

    def openConfig(self):
        dialog = Tkinter.Toplevel(self)
        dialog.geometry(str(DIALOG_WIDTH)+"x"+str(DIALOG_HEIGHT)+"+100+100")
        dialog.minsize(width=DIALOG_WIDTH, height=DIALOG_HEIGHT)
        dialog.title("Preference")
        ft = tkFont.Font(family=FONT_FAMILY, size=DIALOG_FONT_SIZE)
        opt_1 = Tkinter.Radiobutton(dialog, text="Find mean absolute difference (L1) below", font=ft, variable=self.config['dist'], value='l1')
        if self.config['dist'].get() == 'l1':
            opt_1.select()
        else:
            opt_1.deselect()
        opt_1.pack(anchor=Tkinter.W)
        box_1 = Tkinter.Spinbox(dialog, font=ft, textvariable=self.config['th_l1'], from_=0, to=100, increment=1).pack()
        opt_2 = Tkinter.Radiobutton(dialog, text="Find mean square difference (L2) below", font=ft, variable=self.config['dist'], value='l2')
        if self.config['dist'].get() == 'l2':
            opt_2.select()
        else:
            opt_2.deselect()
        opt_2.pack(anchor=Tkinter.W)
        box_2 = Tkinter.Spinbox(dialog, font=ft, textvariable=self.config['th_l2'], from_=0, to=100, increment=1).pack()
        close_button = CloseWindowButton(dialog)


class OpenFolderButton(Tkinter.Button):
    """
    This class creates and owns the photo crawler while opening the target
    folder, which will be passed to other functions for crawling.
    """
    def __init__(self, parent, frame, crawler_config, r, c):
        self.photo_crawler = []
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = parent
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Open folder', font=tkFont.Font(family=FONT_FAMILY, size=BUTTON_FONT_SIZE), command=lambda:self.askdirectory(self.photo_crawler, options, parent, frame, crawler_config))
        self.grid(row=r, column=c, padx=5, pady=5)

    @staticmethod
    def askdirectory(photo_crawler, options, root, frame, crawler_config):
        path = re.escape(tkFileDialog.askdirectory(**options))
        if path:
            del photo_crawler[:]
            photo_crawler.append(util.duplicatePhotoCrawler(path, crawler_config))


class NextBatchButton(Tkinter.Button):
    def __init__(self, parent, batch_photo_frame, selected_photo_frame, photo_crawler, r, c):
        self.cached_canvases = []
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Find duplicates', font=tkFont.Font(family=FONT_FAMILY, size=BUTTON_FONT_SIZE), command=lambda:self.getNextDuplicatedBatch(parent, batch_photo_frame, selected_photo_frame, photo_crawler, self.cached_canvases))
        self.grid(row=r, column=c, padx=5, pady=5)

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
            cached_cv.append(PhotoCanvas(copies[0], selected_photo_frame, DISPLAY_HEIGHT, DISPLAY_WIDTH))
            # show duplicated photo thumbs in batch_photo_frame
            for idx,cp in enumerate(copies):
                cached_cv.append(PhotoCanvas(cp, batch_photo_frame, THUMB_HEIGHT, None, cached_cv[0]))
            # copy pointers of all thumbs to each of them, so they can remove others' highlights when needed
            for cv in cached_cv[1:]:
                cv.setCompetingCanvases(cached_cv[1:])
            # highlight the first picture
            cached_cv[1].highlight()
            root.update_idletasks()
        except StopIteration:
            tkMessageBox.showinfo("Warning", "No more duplicated photos found.")
