#!/usr/local/bin/python2.7

import os,sys,re
import numpy as np
import cv2
import Tkinter, Tkconstants, tkFileDialog
from gui import Canvas
Tkinter.wantobjects = 0
    
def photoCrawler(path):
    prev_photo = None
    for photo in os.popen("ls %s/*" % path).read().splitlines():
        yield (prev_photo, photo)
        prev_photo = photo

def findDuplicatePair(root, canvas, crawler):
    try:
        prev_photo, photo = crawler.next()
        findDuplicate = False
        if prev_photo:
            prev_img = cv2.imread(prev_photo)
            img = cv2.imread(photo)
            if img.shape==prev_img.shape:
                dist = cv2.norm(img, prev_img)/img.size
                if dist<0.01:
                    canvas.loadImages(prev_photo, photo)
                    findDuplicate = True
        if findDuplicate:
            root.update_idletasks()
            root.after(1000, findDuplicatePair, root, canvas, crawler)
        else:
            root.after(0, findDuplicatePair, root, canvas, crawler)
    except:
        return

class Button(object):
    def __init__(self, root, canvas):
        self.bt = Tkinter.Button(root, text='Open folder', command=self.askdirectory)
        self.bt.pack(side=Tkinter.BOTTOM)
        self.options = {}
        self.options['initialdir'] = 'C:\\'
        self.options['mustexist'] = False
        self.options['parent'] = root
        self.options['title'] = 'This is a title'
        self.root = root
        self.canvas = canvas

    def askdirectory(self):
        path = re.escape(tkFileDialog.askdirectory(**self.options))
        crawler = photoCrawler(path)
        findDuplicatePair(self.root, self.canvas, crawler)

if __name__=="__main__":
    root = Tkinter.Tk()
    canvas = Canvas(root)
    button = Button(root, canvas)
    root.mainloop()
