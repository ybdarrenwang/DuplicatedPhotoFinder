Duplicated Photo Finder
=======================
This application is for finding and removing (not yet implemented) similare photos the user has taken consecutively. For now it is assumed that the file names of the photos follow chronological order, and this application only checks if adjacent photos are duplicates.

The user can choose between
1. SIFT & K-Means based cosine distance (default)
2. Mean absolute difference (L1)
3. Mean square difference (L2)
as the measure of image difference.

Platforms tested
----------------
Linux(Ubuntu 14.04), OS X

Prerequisites
-------------
- SciPy
    - `pip install scipy`
- OpenCV for Python (both `opencv` and `opencv_contrib` are needed)
    - [Install on Linux(Ubuntu)](http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/)
    - [Install on OSX](http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/)
- python-opencv package
    - `sudo apt-get install python-opencv`
- Python Image Library
    - Install on Linux(Ubuntu): `sudo apt-get install python-imaging-tk`
    - Install on OS X: `sudo easy_install pip;sudo pip install pillow`
- [Send2Trash -- Send files to trash on all platforms](https://github.com/hsoft/send2trash/)

Execution
---------
Run `python main.py` under command line environment.

Wish list
---------
- Compare rotated pictures
- Compare photos across multiple folder
