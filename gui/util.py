import os
import numpy as np
import cv2
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
    raise StopIteration
