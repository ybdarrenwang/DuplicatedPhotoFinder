import os, sys, math
import numpy as np
from scipy.spatial import distance
import cv2
import Tkinter, tkMessageBox

reload(sys)
sys.setdefaultencoding('utf-8')

class Photo:
    """Object that maintains 
    - photo file path
    - image shape
    - feature vector
    """
    # static variables
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

    def isSimilar(self, ref, distanceMetric, distanceThresh):
        if self.shape!=ref.shape:
            return False
        if distanceMetric=='l1':
            dist = cv2.norm(self.img, ref.img, cv2.NORM_L1)/self.size # average absolute difference, threshold=30
        elif distanceMetric=='l2':
            dist = cv2.norm(self.img, ref.img, cv2.NORM_L2)
            dist = math.sqrt(dist*dist/self.size) # Euclidean distance, threshold=0.01
        elif distanceMetric=='sift':
            compactness,labels,centers = cv2.kmeans(np.concatenate((self.feature,ref.feature)), 16, None, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10), attempts=1, flags=cv2.KMEANS_PP_CENTERS)
            hist1 = [0 for i in range(16)]
            hist2 = [0 for i in range(16)]
            for l in labels[:len(self.feature)]: hist1[l]+=1
            for l in labels[len(self.feature):]: hist2[l]+=1
            dist = distance.cosine(hist1, hist2)
        else:
            tkMessageBox.showinfo("Error", "Unknown distance measure: "+distanceMetric)
            exit("Error: Unknown distance measure: "+config['dist'])
        return (dist<distanceThresh)


class Database:
    # static variables
    distanceMetric = None
    distanceThresh = None
    crawler = None
    duplicated_batch = []

    def __init__(self):
        pass

    def setCrawler(self, path):
        if path:
            self.crawler = self.duplicatedPhotoGenerator(path)
            self.duplicated_batch = []

    def next(self):
        return self.crawler.next()

    def duplicatedPhotoGenerator(self, path):
        """ Return an array with each element being similar Photo objects
        - iterate over all photos in path
        - cache duplicated_batch if found
        - yield group of duplicated_batch
        """
        for photo_file in os.popen("ls %s/*" % path).read().splitlines():
            p = Photo(photo_file)
            if p.img is not None:
                if not self.duplicated_batch or p.isSimilar(self.duplicated_batch[-1], self.distanceMetric.get(), self.distanceThresh):
                    self.duplicated_batch.append(p)
                else:
                    if len(self.duplicated_batch)>1:
                        yield self.duplicated_batch
                    self.duplicated_batch = [p]
        if len(self.duplicated_batch)>1: # the last batch
            yield self.duplicated_batch
        raise StopIteration
