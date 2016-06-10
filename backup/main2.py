#!/usr/local/bin/python2.7

import os,sys,re
import numpy as np
import cv2
import Tkinter
from PIL import Image, ImageTk
from gui import Canvas
import time

root = Tkinter.Tk()
canvas1 = Tkinter.Canvas(root, width=250, height=250)
canvas1.pack(side=Tkinter.LEFT)
canvas2 = Tkinter.Canvas(root, width=250, height=250)
canvas2.pack(side=Tkinter.LEFT)
thumb = [None, None]
img = [None, None]

def photoCrawler(path):
    prev_photo = None
    for photo in os.popen("ls %s/*" % path).read().splitlines():
        yield (prev_photo, photo)
        prev_photo = photo

crawler = photoCrawler("~/Dropbox/Camera\ Uploads/")

def findDuplicatePair():
    photo1, photo2 = crawler.next()
    if photo1:
        print photo1
        print photo2
        tmp = Image.open(photo1).resize((250, 250), Image.ANTIALIAS)
        thumb[0] = ImageTk.PhotoImage(tmp)
        if img[0]==None:
            img[0] = canvas1.create_image(0, 0, image = thumb[0], anchor='nw')
        else:
            canvas1.itemconfig(img[0], image = thumb[0])
        tmp = Image.open(photo2).resize((250, 250), Image.ANTIALIAS)
        thumb[1] = ImageTk.PhotoImage(tmp)
        if not img[1]:
            img[1] = canvas2.create_image(0, 0, image = thumb[1], anchor='nw')
        else:
            canvas2.itemconfig(img[1], image = thumb[1])
    root.update_idletasks()
    root.after(5000, findDuplicatePair)

findDuplicatePair()
root.mainloop()
