import re
import Tkinter, Tkconstants
import gui_methods

class OpenFolderButton(Tkinter.Button):
    def __init__(self, parent, frame):
        self.crawler = []
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = parent
        Tkinter.Button.__init__(self, parent, text='Open folder', command=lambda:gui_methods.askdirectory(self.crawler, options, parent, frame))
        self.pack(side=Tkinter.LEFT)

class NextBatchButton(Tkinter.Button):
    def __init__(self, parent, frame, bt):
        self.cachedPics = []
        Tkinter.Button.__init__(self, parent, text='Next batch', command=lambda:gui_methods.getNextDuplicatedBatch(parent, frame, bt, self.cachedPics))
        self.pack(side=Tkinter.LEFT)
