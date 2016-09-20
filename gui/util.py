import os, sys, math
import numpy as np
import cv2

reload(sys)
sys.setdefaultencoding('utf-8')

def duplicatePhotoCrawler(path, config):
    """
    - iterate over all photos in path
    - cache copies if found
    - yield group of copies
    """
    copies = []
    for photo in os.popen("ls %s/*" % path).read().splitlines():
        img = cv2.imread(photo)
        if img!=None:
            if copies:
                if img.shape==copies[-1]["shape"]:
                    prev_img = cv2.imread(copies[-1]["path"])
                    if config['dist'].get()=='l1':
                        dist = cv2.norm(img, prev_img, cv2.NORM_L1)/img.size # average absolute difference, threshold=30
                        th = config['th_l1'].get()
                    elif config['dist'].get()=='l2':
                        dist = cv2.norm(img, prev_img, cv2.NORM_L2)
                        dist = math.sqrt(dist*dist/img.size) # Euclidean distance, threshold=0.01
                        th = config['th_l2'].get()
                    else:
                        tkMessageBox.showinfo("Error", "Unknown distance measure: "+config['dist'].get())
                        exit("Error: Unknown distance measure: "+config['dist'].get())
                    if dist<th:
                        copies.append({"path":photo, "shape":img.shape})
                        continue
                if len(copies)>1:
                    yield copies
            copies = [{"path":photo, "shape":img.shape}]
    if len(copies)>1: # the last batch of copies
        yield copies
    raise StopIteration
