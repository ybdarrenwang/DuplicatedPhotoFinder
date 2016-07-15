import os
import numpy as np
import cv2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def duplicatePhotoCrawler(path):
    """
    - iterate over all photos in path
    - cache copies if found
    - yield group of copies
    """
    copies = []
    for photo in os.popen("ls %s/*" % path).read().splitlines():
        img = cv2.imread(photo)
        if copies:
            if img.shape==copies[-1]["shape"]:
                prev_img = cv2.imread(copies[-1]["path"])
                dist = cv2.norm(img, prev_img)/img.size
                if dist<0.007:
                    copies.append({"path":photo, "shape":img.shape})
                    continue
            if len(copies)>1:
                yield copies
        copies = [{"path":photo, "shape":img.shape}]
    if len(copies)>1: # the last batch of copies
        yield copies
    raise StopIteration
