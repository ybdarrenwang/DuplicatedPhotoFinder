import os
import numpy as np
import cv2
from canvas import Canvas
#Tkinter.wantobjects = 0
import time, gc
    
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
    raise StopIteration

def findDuplicate(root, frame, crawler, cache):
    if len(cache)>0:
        for cv in cache:
            cv.destroy()
    copies = crawler.next()
    if not copies:
        return
    cache = []
    for idx,cp in enumerate(copies):
        cache.append(Canvas(frame, 250, 250))
        cache[-1].loadImages(cp)
    root.update_idletasks()
    time.sleep(3)
    for cv in cache:
        cv.destroy()
    #root.after(0, findDuplicate, root, frame, crawler)
