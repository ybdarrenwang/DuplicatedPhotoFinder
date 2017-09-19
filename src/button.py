import os, re
import Tkinter, tkFont, tkFileDialog, tkMessageBox
from canvas import PhotoCanvas
from config import *
import database
from send2trash import send2trash


class OpenFolderButton(Tkinter.Button):
    """
    This class owns the pointer to photo database folder path
    """
    def __init__(self, parent, frame, db, next_batch_button, r, c):
        self.db = db
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = parent
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Open folder', font=tkFont.Font(family=FONT_FAMILY, size=BUTTON_FONT_SIZE), command=lambda:self.askdirectory(options, next_batch_button))
        self.grid(row=r, column=c, padx=5, pady=5)

    def askdirectory(self, options, next_batch_button):
        path = re.escape(tkFileDialog.askdirectory(**options))
        self.db.setCrawler(path)
        next_batch_button.getNextDuplicatedBatch()

class NextBatchButton(Tkinter.Button):
    """
    Note: this class owns
    1) canvases to display photos
    2) photo info label
    3) delete photo button
    """
    def __init__(self, parent, batch_photo_frame, selected_photo_frame, selected_photo_info_frame, db, r, c):
        """
        batch_photo_frame: to display the thumbs of all duplicated photos
        selected_photo_frame: to display the selected photo
        selected_photo_label: to display the file info of selected photo
        cv4display: a list of canvases; cv4display[0] display the selected photo, others are photo thumbs.
        """
        self.cv4display = []
        self.db = db
        # create photo info label and delete photo button
        self.photo_info = Tkinter.Label(selected_photo_info_frame, height=NUM_INFO_LINE, font=tkFont.Font(family=FONT_FAMILY, size=DIALOG_FONT_SIZE), background="white")
        self.photo_info.pack(expand=True, padx=5, pady=5)
        self.photo_info.pack_forget() # hide photo info whenever photo is absent
        self.button_delete = DeletePhotoButton(selected_photo_info_frame, self.db, self.cv4display)
        self.button_delete.pack_forget() # hide delete button whenever photo is absent
        # create self
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Find duplicates', font=tkFont.Font(family=FONT_FAMILY, size=BUTTON_FONT_SIZE), command=lambda:self.getNextDuplicatedBatch())
        self.grid(row=r, column=c, padx=5, pady=5)
        # set display frames
        self.batch_photo_frame = batch_photo_frame
        self.selected_photo_frame = selected_photo_frame

    def getNextDuplicatedBatch(self):
        if self.db.crawler==None:
            tkMessageBox.showinfo("Warning", "Please choose a folder with more than 1 pictures inside!")
            return
        if self.cv4display: # delete canvases of previous batch
            for cv in self.cv4display:
                cv.destroy()
            del self.cv4display[:]
        try:
            self.photo_info.pack_forget()
            self.button_delete.pack_forget()
            # fetch next batch
            copies = self.db.next()
            # show the first photo in selected_photo_frame
            self.cv4display.append(PhotoCanvas(copies[0], self.selected_photo_frame, DISPLAY_HEIGHT, DISPLAY_WIDTH))
            # show duplicated photo thumbs in batch_photo_frame
            for idx,cp in enumerate(copies):
                self.cv4display.append(PhotoCanvas(cp, self.batch_photo_frame, THUMB_HEIGHT-2*MARGIN, None, self.cv4display[0], self.photo_info))
            # copy pointers of all thumbs to each of them, so they can remove others' highlights when needed
            for cv in self.cv4display[1:]:
                cv.setCompetingCanvases(self.cv4display[1:])
            # highlight the first picture
            self.cv4display[1].highlight()
            self.photo_info.pack()
            self.button_delete.pack()
        except StopIteration:
            tkMessageBox.showinfo("Warning", "No more duplicated photos found.")


class DeletePhotoButton(Tkinter.Button):
    """
    cv4display: a list of canvases; cv4display[0] display the selected photo, others are photo thumbs.
    """
    def __init__(self, parent, db, cv4display):
        self.db = db
        self.cv4display = cv4display
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Recycle photo', font=tkFont.Font(family=FONT_FAMILY, size=DIALOG_FONT_SIZE), command=lambda:self.deletePhoto())
        self.pack(side=Tkinter.BOTTOM, padx=5, pady=5)

    def deletePhoto(self):
        if len(self.cv4display)==0:
            tkMessageBox.showinfo("Warning", "No more photos from this batch!")
            return
        for i in range(len(self.db.duplicated_batch)):
            if self.cv4display[i+1].isSelected:
                self.cv4display[i+1].info_label.configure(text='')
                self.cv4display[i+1].destroy()
                del self.cv4display[i+1]
                send2trash(self.db.duplicated_batch[i]['path'])
                del self.db.duplicated_batch[i]
                break
        if len(self.cv4display)>1:
            # copy pointers of all thumbs to each of them, so they can remove others' highlights when needed
            for cv in self.cv4display[1:]:
                cv.setCompetingCanvases(self.cv4display[1:])
            # highlight the first picture
            self.cv4display[1].highlight()
        else: # entire batch deleted
            self.cv4display[0].destroy()
            del self.cv4display[0]
            del self.db.duplicated_batch[0]


class ConfigButton(Tkinter.Button):
    """Configure how similarity is calculated
    Default: Find SIFT K-Means cosine distance below SIFT_THRESH.
    Note this class owns the pointer to photo database configuration.
    """
    def __init__(self, parent, db, r, c):
        self.db = db
        self.db.distanceMetric = Tkinter.StringVar()
        self.db.distanceMetric.set('sift')
        self.db.distanceThresh = SIFT_THRESH
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Preference...', font=tkFont.Font(family=FONT_FAMILY, size=BUTTON_FONT_SIZE), command=self.openConfig)
        self.grid(row=r, column=c, padx=5, pady=5)

    def openConfig(self):
        dialog = Tkinter.Toplevel(self)
        dialog.geometry(str(DIALOG_WIDTH)+"x"+str(DIALOG_HEIGHT)+"+100+100")
        dialog.minsize(width=DIALOG_WIDTH, height=DIALOG_HEIGHT)
        dialog.title("Preference")
        ft = tkFont.Font(family=FONT_FAMILY, size=DIALOG_FONT_SIZE)
        # config L1 distance
        opt_1 = Tkinter.Radiobutton(dialog, text="Find mean absolute difference (L1) below "+str(L1_THRESH), font=ft, variable=self.db.distanceMetric, value='l1')
        if self.db.distanceMetric.get() == 'l1':
            opt_1.select()
        else:
            opt_1.deselect()
        opt_1.pack(anchor=Tkinter.W)
        # config L2 distance
        opt_2 = Tkinter.Radiobutton(dialog, text="Find mean square difference (L2) below "+str(L2_THRESH), font=ft, variable=self.db.distanceMetric, value='l2')
        if self.db.distanceMetric.get() == 'l2':
            opt_2.select()
        else:
            opt_2.deselect()
        opt_2.pack(anchor=Tkinter.W)
        # config SIFT K-Means cosine distance
        opt_3 = Tkinter.Radiobutton(dialog, text="Find SIFT K-Means cosine distance below "+str(SIFT_THRESH), font=ft, variable=self.db.distanceMetric, value='sift')
        if self.db.distanceMetric.get() == 'sift':
            opt_3.select()
        else:
            opt_3.deselect()
        opt_3.pack(anchor=Tkinter.W)
        # close window button
        close_button = CloseWindowButton(dialog)


class CloseWindowButton(Tkinter.Button):
    def __init__(self, parent):
        self.root = parent
        Tkinter.Button.__init__(self, parent, width=BUTTON_WIDTH, text='Done', font=tkFont.Font(family=FONT_FAMILY, size=DIALOG_FONT_SIZE), command=self.close)
        self.pack(side=Tkinter.RIGHT, padx=5, pady=5)

    def close(self):
        self.root.destroy()
