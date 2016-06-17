import sys, Tkinter
sys.path.insert(0, "./gui/")
from button import OpenFolderButton, NextBatchButton

#Tkinter.wantobjects = 0

if __name__=="__main__":
    root = Tkinter.Tk()
    frame = Tkinter.Frame(root, relief=Tkinter.RAISED, borderwidth=1)
    frame.pack(fill=Tkinter.BOTH, expand=True)
    #canvas = Canvas(frame)
    #button = Button.loadFolder(root, canvas)
    button1 = OpenFolderButton(root, frame)
    button2 = NextBatchButton(root, frame, button1)
    root.mainloop()
