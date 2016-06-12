import os
import numpy as np
import cv2
import Tkinter
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
