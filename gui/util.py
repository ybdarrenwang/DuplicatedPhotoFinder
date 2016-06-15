import os
import numpy as np
import cv2
from canvas import Canvas
#Tkinter.wantobjects = 0
    
def duplicatePhotoCrawler(path):
    """
    - iterate over all photos in path
    - cache copies if found
    - yield group of copies
    """
    copies = []
    for photo in os.popen("ls %s/*" % path).read().splitlines():
        if copies:
            prev_img = cv2.imread(copies[-1])
            img = cv2.imread(photo)
            if img.shape==prev_img.shape:
                dist = cv2.norm(img, prev_img)/img.size
                if dist<0.01:
                    copies.append(photo)
                else:
                    if len(copies)>1:
                        yield copies
                    copies = [photo]
            else:
                if len(copies)>1:
                    yield copies
                copies = [photo]
        else:
            copies = [photo]
    if len(copies)>1: # the last batch of copies
        yield copies

def findDuplicate(root, frame, crawler):
    try:
        copies = crawler.next()
        canvases = []
        for idx,cp in enumerate(copies):
            canvases.append(Canvas(frame, 250, 250))
            canvases[-1].loadImages(cp)
        root.update_idletasks()
        root.after(1000, findDuplicatePair, root, frame, crawler)
    except:
        return
"""
def findDuplicate(root, canvas, crawler):
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
"""
