Duplicated Photo Finder
=======================
Find, browse and manually remove similare photos in a folder.

It is assumed that the filenames follow chronological order, and the algorithm only checks whether adjcent photos are highly similar. The use case is when someone has taken similar photos consecutively for later choose and edit purpose.

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

Known issues
------------
1. Randomness in K-means algorithm would make distance of same pair of photos different for each run.
2. Rotated photos would be displayed in original shape.
