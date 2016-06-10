#!/usr/local/bin/python2.7

import os,sys,re
import numpy as np
import cv2
import Tkinter
from PIL import Image, ImageTk
from gui import GUI
import time

def photoCrawler(path):
    prev_photo = None
    for photo in os.popen("ls %s/*" % path).read().splitlines():
        yield (photo, prev_photo)
        prev_photo = photo

def findDuplicatePair(root, canvases):
    root.update_idletasks()
    root.after(1000, findDuplicatePair(root, canvases))

if __name__=="__main__":
    #root = Tkinter.Tk()
    #label = Tkinter.Label(root, text="Tk's job!!", width="30", height="5")
    #label.pack()
    prev_photo = None
    prev_img = None
    root = Tkinter.Tk()
    root.mainloop()
    for photo in os.popen("ls ~/Dropbox/Camera\ Uploads/*").read().splitlines():
        img = cv2.imread(photo)
        if prev_photo and img.shape==prev_img.shape:
            dist = cv2.norm(img, prev_img)/img.size
            if dist<0.01:
                #root = Tkinter.Tk()
                _canvas1 = Tkinter.Canvas(root, width=250, height=250)
                _canvas1.pack(side=Tkinter.LEFT)
                _canvas2 = Tkinter.Canvas(root, width=250, height=250)
                _canvas2.pack(side=Tkinter.LEFT)
                #_gui.loadImages(prev_photo, photo)
                _image = Image.open(photo).resize((250, 250), Image.ANTIALIAS)
                _file1 = ImageTk.PhotoImage(_image)
                _canvas1.create_image(0, 0, image = _file1, anchor='nw')
                _image = Image.open(prev_photo).resize((250, 250), Image.ANTIALIAS)
                _file2 = ImageTk.PhotoImage(_image)
                _canvas2.create_image(0, 0, image = _file2, anchor='nw')
                #root.mainloop()
                root.update_idletasks()
                time.sleep(2)
                print "======"
                print photo
                print prev_photo
                print "======"
        prev_photo = photo
        prev_img = img
