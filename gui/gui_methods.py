import Tkinter, tkFileDialog
from canvas import Canvas
import re
import util

def askdirectory(crawler, options, root, frame):
    path = re.escape(tkFileDialog.askdirectory(**options))
    crawler.append(util.duplicatePhotoCrawler(path))

def getNextDuplicatedBatch(root, frame, bt, cache):
    if cache:
        for cv in cache:
            cv.destroy()
        del cache[:]
    copies = bt.crawler[-1].next()
    if not copies:
        return
    for idx,cp in enumerate(copies):
        height, width, channel = cp["shape"]
        ratio = max([height, width])/250.0
        cache.append(Canvas(frame, int(width/ratio), int(height/ratio)))
        cache[-1].loadImages(cp["path"])
    root.update_idletasks()
