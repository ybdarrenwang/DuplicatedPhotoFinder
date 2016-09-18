import re
import Tkinter, Tkconstants, tkFont
import gui_methods

class OpenFolderButton(Tkinter.Button):
    def __init__(self, parent, frame):
        self.crawler = []
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = parent
        ft = tkFont.Font(family='courier', size=18)
        Tkinter.Button.__init__(self, parent, width=17, text='Open folder', font=ft, command=lambda:gui_methods.askdirectory(self.crawler, options, parent, frame))
        self.pack(side=Tkinter.LEFT)

class NextBatchButton(Tkinter.Button):
    def __init__(self, parent, batch_photo_frame, selected_photo_frame, bt):
        self.cachedPics = []
        ft = tkFont.Font(family='courier', size=18)
        Tkinter.Button.__init__(self, parent, width=17, text='Find duplicates', font=ft, command=lambda:gui_methods.getNextDuplicatedBatch(parent, batch_photo_frame, selected_photo_frame, bt, self.cachedPics))
        self.pack(side=Tkinter.RIGHT)
