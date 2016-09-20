Duplicated Photo Finder
=======================
This application is for finding and removing (not yet implemented) similare photos the user has taken consecutively. For now it is assumed that the file names of the photos follow chronological order, and this application only checks if adjacent photos are duplicates.

The user can choose between mean absolute difference (L1) or mean square difference (L2) as the measure of image difference.

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
- "Delete picture" button
- "Rotate picture" button
- Compare photos across multiple folder
- Calculate image similarity by histogram comparison (`cv2.compareHist()`)
    - Extension: use Mutual Information or Entropy for histogram comparison
