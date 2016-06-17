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
        cache.append(Canvas(frame, 250, 250))
        cache[-1].loadImages(cp)
    root.update_idletasks()
