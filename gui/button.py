import re
import Tkinter, Tkconstants
import gui_methods

class Button(object):
    def __init__(self, bt):
        self.bt = bt
        self.cache = None

    @classmethod
    def loadFolder(cls, parent, frame):
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = parent
        bt = Tkinter.Button(parent, text='Load folder', command=lambda:gui_methods.askdirectory(bt, options, parent, frame))
        bt.pack(side=Tkinter.BOTTOM)
        return cls(bt)

    @classmethod
    def nextBatch(cls, parent, frame, crawler):
        bt = Tkinter.Button(parent, text='Next batch', command=lambda:gui_methods.getNextDuplicatedBatch(bt, parent, frame, crawler))
        bt.pack(side=Tkinter.BOTTOM)
        return cls(bt)
