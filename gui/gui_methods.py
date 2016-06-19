import Tkinter, tkFileDialog, tkMessageBox
from canvas import Canvas
import re
import util

def askdirectory(crawler, options, root, frame):
    path = re.escape(tkFileDialog.askdirectory(**options))
    if path:
        del crawler[:]
        crawler.append(util.duplicatePhotoCrawler(path))

def getNextDuplicatedBatch(root, frame, bt, cache):
    if cache:
        for cv in cache:
            cv.destroy()
        del cache[:]
    if len(bt.crawler)==0:
        tkMessageBox.showinfo("Warning", "Please choose a folder.")
        return
    copies = bt.crawler[-1].next()
    if not copies:
        tkMessageBox.showinfo("Warning", "No more duplicated photos found.")
        return
    for idx,cp in enumerate(copies):
        height, width, channel = cp["shape"]
        ratio = max([height, width])/250.0
        cache.append(Canvas(frame, int(width/ratio), int(height/ratio)))
        cache[-1].loadImages(cp["path"])
    root.update_idletasks()
