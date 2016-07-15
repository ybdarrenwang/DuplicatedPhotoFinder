import Tkinter, tkFileDialog, tkMessageBox
from canvas import Canvas
import re
import util

def askdirectory(crawler, options, root, frame):
    path = re.escape(tkFileDialog.askdirectory(**options))
    if path:
        del crawler[:]
        crawler.append(util.duplicatePhotoCrawler(path))

def getNextDuplicatedBatch(root, batch_photo_frame, selected_photo_frame, bt, cache):
    if cache:
        for cv in cache:
            cv.destroy()
        del cache[:]
    if len(bt.crawler)==0:
        tkMessageBox.showinfo("Warning", "Please choose a folder.")
        return
    try:
        copies = bt.crawler[-1].next()
        # show duplicated photos in batch_photo_frame
        for idx,cp in enumerate(copies):
            height, width, channel = cp["shape"]
            ratio = height/100.0
            cache.append(Canvas(batch_photo_frame, int(width/ratio), int(height/ratio)))
            cache[-1].loadImages(cp["path"])
        # show the first photo in selected_photo_frame
        height, width, channel = copies[0]["shape"]
        ratio = height/450.0
        cache.append(Canvas(selected_photo_frame, int(width/ratio), int(height/ratio), True))
        cache[-1].loadImages(copies[0]["path"])
        root.update_idletasks()
    except StopIteration:
        tkMessageBox.showinfo("Warning", "No more duplicated photos found.")
