Duplicated Photo Finder
=======================
This application is for finding and removing (not yet implemented) duplicated photos. Note it is assumed that the file name of the photos follows chronological order, and this application only checks if adjacent photos are duplicates.

Right now I only use the average of absolute difference as the similarity measure of two images.

Platforms tested
----------------
Linux(Ubuntu 14.04), OS X

Prerequisites
-------------
- OpenCV for Python
    - [Install on Linux(Ubuntu)](http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/)
    - [Install on OSX](http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/)
- Python Image Library
    - Install on Linux(Ubuntu): `sudo apt-get install python-imaging-tk`
    - Install on OS X: `sudo easy_install pip;sudo pip install pillow`

Execution
---------
Run `python main.py` under command line environment.

Wish list
---------
- "Delete picture" function
- "Rotate picture" function
- Calculate image similarity by histogram comparison (`cv2.compareHist()`)
    - Extension: use Mutual Information or Entropy for histogram comparison
