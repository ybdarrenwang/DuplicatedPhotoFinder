import re
import Tkinter, Tkconstants
import gui_methods

class Button(object):
    def __init__(self, bt, options):
        self.bt = bt
        self.options = options

    @classmethod
    def loadFolder(cls, parent, frame):
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = parent
        #options['title'] = 'This is a title'
        bt = Tkinter.Button(parent, text='Load folder', command=lambda:gui_methods.askdirectory(options, parent, frame))
        bt.pack(side=Tkinter.BOTTOM)
        return cls(bt, options)
