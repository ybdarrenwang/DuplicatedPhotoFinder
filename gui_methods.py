import Tkinter, tkFileDialog
import re
import util

def askdirectory(options, root, frame):
    path = re.escape(tkFileDialog.askdirectory(**options))
    crawler = util.duplicatePhotoCrawler(path)
    util.findDuplicate(root, frame, crawler)
