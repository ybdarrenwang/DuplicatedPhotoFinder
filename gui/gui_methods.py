import Tkinter, tkFileDialog
import re
import util

def askdirectory(bt, options, root, frame):
    path = re.escape(tkFileDialog.askdirectory(**options))
    bt.cache = util.duplicatePhotoCrawler(path)
    #util.findDuplicate(root, frame, crawler)

def getNextDuplicatedBatch(bt, root, frame, crawler):
    util.findDuplicate(root, frame, crawler, bt.cache)
