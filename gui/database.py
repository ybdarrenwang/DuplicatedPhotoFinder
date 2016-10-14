import os, sys, math
import numpy as np
import cv2
import Tkinter

reload(sys)
sys.setdefaultencoding('utf-8')


class Database:
    # static variable, so it'd be passed along disregarding photo folder changes
    config = {'dist':'l1', 'th_l1':30, 'th_l2':50}
    crawler = None
    duplicated_batch = []

    def __init__(self):
        pass

    def setCrawler(self, path):
        self.crawler = self.duplicatedPhotoGenerator(path)
        self.duplicated_batch = []

    def next(self):
        return self.crawler.next()

    def duplicatedPhotoGenerator(self, path):
        """
        - iterate over all photos in path
        - cache duplicated_batch if found
        - yield group of duplicated_batch
        """
        for photo in os.popen("ls %s/*" % path).read().splitlines():
            img = cv2.imread(photo)
            if img!=None:
                if self.duplicated_batch:
                    if img.shape==self.duplicated_batch[-1]["shape"]:
                        prev_img = cv2.imread(self.duplicated_batch[-1]["path"])
                        if self.config['dist']=='l1':
                            dist = cv2.norm(img, prev_img, cv2.NORM_L1)/img.size # average absolute difference, threshold=30
                            th = self.config['th_l1']
                        elif self.config['dist']=='l2':
                            dist = cv2.norm(img, prev_img, cv2.NORM_L2)
                            dist = math.sqrt(dist*dist/img.size) # Euclidean distance, threshold=0.01
                            th = self.config['th_l2']
                        else:
                            tkMessageBox.showinfo("Error", "Unknown distance measure: "+self.config['dist'])
                            exit("Error: Unknown distance measure: "+self.config['dist'])
                        if dist<th:
                            self.duplicated_batch.append({"path":photo, "shape":img.shape})
                            continue
                    if len(self.duplicated_batch)>1:
                        yield self.duplicated_batch
                self.duplicated_batch = [{"path":photo, "shape":img.shape}]
        if len(self.duplicated_batch)>1: # the last batch
            yield self.duplicated_batch
        raise StopIteration
