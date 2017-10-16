import os, sys, re, math
import numpy as np
from scipy.spatial import distance
import cv2
import Tkinter, tkMessageBox
from config import *

reload(sys)
sys.setdefaultencoding('utf-8')

class Photo:
    """ A structure maintaining photo related attributes.

    # Member objects
        path: Photo file path.
        img: CV2 image object.
        shape: Image shape.
        size: Image size.
        feature: Feature vector.
    """
    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(path)
        if self.img is not None:
            self.shape = self.img.shape
            self.size = self.img.size
        else:
            self.shape = None
            self.size = None
        self.feature = None


class Database:
    """ Load and process photos from a directory.

    # Member objects
        sift (static): A CV2 SIFT operator object.
        DIST_THRESH (static): photos with distance < DIST_THRESH are considered similar.
        progress_bar: A ttk.Progressbar object for displaying progress.
        crawler: A Python generator, emits a batch of similar photos per request.
    """
    sift = cv2.xfeatures2d.SIFT_create()
    DIST_THRESH = SIFT_THRESH
    crawler = None

    def __init__(self, progress_bar):
        self.progress_bar = progress_bar

    def load(self, path):
        if path:
            self.crawler = self.duplicatedPhotoGenerator(path)
        else:
            self.crawler = None

    def getNextDuplicatedBatch(self):
        if self.crawler is not None:
            return self.crawler.next()

    def isSimilarPhotos(self, p1, p2):
        """ 
        1. Extract SIFT features for both photos.
        2. Run k-means clustering over all SIFT feature points from both photos.
        3. Collect the distribution (histogram) of feature points over different
           clusters as its signature.
        4. If the cosine distance between 2 histograms belows threshold, then
           similar.

        # Arguments:
            p1: The 1st photo.
            p2: The 2nd photo.

        # Returns:
            True if 2 photos are similar; False otherwise.
        """
        if p1.feature is None:
            gray = cv2.cvtColor(p1.img, cv2.COLOR_BGR2GRAY)
            keypoint, p1.feature = self.sift.detectAndCompute(gray, None)
        if p2.feature is None:
            gray = cv2.cvtColor(p2.img, cv2.COLOR_BGR2GRAY)
            keypoint, p2.feature = self.sift.detectAndCompute(gray, None)
        compactness,labels,centers = cv2.kmeans(np.concatenate((p1.feature,p2.feature)), 16, None, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10), attempts=1, flags=cv2.KMEANS_PP_CENTERS)
        hist1 = [0 for i in range(16)]
        hist2 = [0 for i in range(16)]
        for l in labels[:len(p1.feature), 0]: hist1[l]+=1
        for l in labels[len(p1.feature):, 0]: hist2[l]+=1
        dist = distance.cosine(hist1, hist2)
        return (dist<self.DIST_THRESH)

    def duplicatedPhotoGenerator(self, path):
        """ Iterate over all photos in directory. Yield similar photos as an array of Photo objects. """
        prev_photo = None
        duplicated_batch = []
        self.progress_bar.start()
        total_num_files = len(os.popen("ls %s/*" % re.escape(path)).read().splitlines())
        for idx, photo_file in enumerate(os.popen("ls %s/*" % re.escape(path)).read().splitlines()):
            self.progress_bar["value"] = 100.0*idx/total_num_files
            self.progress_bar.update()
            photo = Photo(photo_file)
            if photo.img is None:
                continue
            if prev_photo is not None and self.isSimilarPhotos(prev_photo, photo):
                duplicated_batch.append(photo)
            else:
                if len(duplicated_batch)>1:
                    self.progress_bar.stop()
                    yield duplicated_batch
                    self.progress_bar.start()
                duplicated_batch = [photo]
            prev_photo = photo
        self.progress_bar.stop()
        if len(duplicated_batch)>1: # the last batch
            yield duplicated_batch
        raise StopIteration
