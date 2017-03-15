import os, sys, math
import numpy as np
from scipy.spatial import distance
#import sklearn
import cv2
import Tkinter

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
            # extract SIFT feature
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            keypoint, descriptors = self.sift.detectAndCompute(gray, None)
            #kmeans = sklearn.cluster.KMeans(n_clusters=4, random_state=0).fit(descriptors)
            #self.feature = np.squeeze(np.asarray(kmeans.cluster_centers_))
            foo, bar, means = cv2.kmeans(descriptors, 8, None, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10), attempts=1, flags=cv2.KMEANS_RANDOM_CENTERS)
            self.feature = means.flatten()

    def isSimilar(self, ref, config):
        """
        if self.shape!=ref.shape:
            return False
        if config['dist']=='l1':
            dist = cv2.norm(self.img, ref.img, cv2.NORM_L1)/self.size # average absolute difference, threshold=30
            th = config['th_l1']
        elif config['dist']=='l2':
            dist = cv2.norm(self.img, ref.img, cv2.NORM_L2)
            dist = math.sqrt(dist*dist/self.size) # Euclidean distance, threshold=0.01
            th = config['th_l2']
        else:
            tkMessageBox.showinfo("Error", "Unknown distance measure: "+config['dist'])
            exit("Error: Unknown distance measure: "+config['dist'])
        return (dist<th)
        """
        return (distance.cosine(self.feature, ref.feature)<0.4)



class Database:
    # static variables
    config = {'dist':'l1', 'th_l1':30, 'th_l2':50}
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
                if not self.duplicated_batch or p.isSimilar(self.duplicated_batch[-1], self.config):
                    self.duplicated_batch.append(p)
                else:
                    if len(self.duplicated_batch)>1:
                        yield self.duplicated_batch
                    self.duplicated_batch = [p]
        if len(self.duplicated_batch)>1: # the last batch
            yield self.duplicated_batch
        raise StopIteration
