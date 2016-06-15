import Tkinter
from gui import Button, Canvas

#Tkinter.wantobjects = 0

def findDuplicate(root, frame, crawler):
    try:
        copies = crawler.next()
        canvases = []
        for cp in copies:
            print cp
            canvas = Canvas(frame, 250, 250)
            canvas.loadImages(cp)
            #canvases.append(Canvas(frame, 250, 250))
            #canvases[-1].loadImages(cp)
        root.update_idletasks()
        root.after(1000, findDuplicatePair, root, frame, crawler)
    except:
        return

if __name__=="__main__":
    root = Tkinter.Tk()
    frame = Tkinter.Frame(root, relief=Tkinter.RAISED, borderwidth=1)
    frame.pack(fill=Tkinter.BOTH, expand=True)
    #canvas = Canvas(frame)
    #button = Button.loadFolder(root, canvas)
    button = Button.loadFolder(root, frame)
    root.mainloop()
