import Tkinter, tkFileDialog
import re
import util

def askdirectory(options, root, canvas):
    path = re.escape(tkFileDialog.askdirectory(**options))
    crawler = util.photoCrawler(path)
    util.findDuplicatePair(root, canvas, crawler)
