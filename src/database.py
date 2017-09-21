import os, sys, re, math
import numpy as np
from scipy.spatial import distance
import cv2
import Tkinter, tkMessageBox

reload(sys)
sys.setdefaultencoding('utf-8')

class Photo:
    """
    Object that maintains 
    - Photo file path (self.path)
    - CV2 image object (self.img)
    - Image shape (self.shape)
    - Image size (self.size)
    - SIFT feature vector (self.feature)
    """
    sift = cv2.xfeatures2d.SIFT_create()

    def __init__(self, path):
        print "Loading "+path
        self.path = path
        self.img = cv2.imread(path)
        if self.img is not None:
            self.shape = self.img.shape
            self.size = self.img.size
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            keypoint, self.feature = self.sift.detectAndCompute(gray, None)


class Database:
    """
    This class owns the list of photo objects, photo clustering algorithm, and
    the generator for emitting duplicated photo batches. Note the
    parameters can be set by ConfigButton class object.
    """
    DIST_METRIC = None
    DIST_THRESH = None
    crawler = None
    duplicated_batch = []

    def __init__(self):
        pass

    def load(self, path):
        self.crawler = None
        if path:
            self.crawler = self.duplicatedPhotoGenerator(path)
            self.duplicated_batch = []

    def getNextDuplicatedBatch(self):
        if self.crawler is not None:
            return self.crawler.next()

    def isSimilarPhotos(self, p1, p2):
        if p1.shape!=p2.shape:
            return False
        if self.DIST_METRIC.get()=='l1':
            dist = cv2.norm(p1.img, p2.img, cv2.NORM_L1)/p1.size # average absolute difference, threshold=30
        elif self.DIST_METRIC.get()=='l2':
            dist = cv2.norm(p1.img, p2.img, cv2.NORM_L2)
            dist = math.sqrt(dist*dist/p1.size) # Euclidean distance, threshold=0.01
        elif self.DIST_METRIC.get()=='sift':
            compactness,labels,centers = cv2.kmeans(np.concatenate((p1.feature,p2.feature)), 16, None, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10), attempts=1, flags=cv2.KMEANS_PP_CENTERS)
            hist1 = [0 for i in range(16)]
            hist2 = [0 for i in range(16)]
            for l in labels[:len(p1.feature)]: hist1[l]+=1
            for l in labels[len(p1.feature):]: hist2[l]+=1
            dist = distance.cosine(hist1, hist2)
        else:
            tkMessageBox.showinfo("Error", "Unknown distance measure: "+self.DIST_METRIC.get())
            exit("Error: Unknown distance measure: "+config['dist'])
        return (dist<self.DIST_THRESH)

    def duplicatedPhotoGenerator(self, path):
        """ Return an array with each element being similar Photo objects
        - iterate over all photos in path
        - cache duplicated_batch if found
        - yield group of duplicated_batch
        """
        prev_photo = None
        for photo_file in os.popen("ls %s/*" % re.escape(path)).read().splitlines():
            photo = Photo(photo_file)
            if photo.img is None:
                continue
            if prev_photo is not None and self.isSimilarPhotos(prev_photo, photo):
                self.duplicated_batch.append(photo)
            else:
                if len(self.duplicated_batch)>1:
                    yield self.duplicated_batch
                self.duplicated_batch = [photo]
            prev_photo = photo
        if len(self.duplicated_batch)>1: # the last batch
            yield self.duplicated_batch
        raise StopIteration
