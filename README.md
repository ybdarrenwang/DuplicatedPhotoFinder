Duplicated Photo Finder
=======================

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
    - Install on OSX: `sudo easy_install pip;sudo pip install pillow`

To-do
-----
- Delete picture function
- Rotate picture function
- Implement other image similarity metrics
    - Euclidean distance
    - Normalized Cross Correlation
    - Compare histogram
        - OpenCV method: compareHist()
        - Extension: use Mutual Information or Entropy for histogram comparison
- Measure image quality between original and disroted image?
    - Structural Similarity Index (SSIM)
