import Tkinter
from gui import Canvas, Button

Tkinter.wantobjects = 0

if __name__=="__main__":
    root = Tkinter.Tk()
    canvas = Canvas(root)
    button = Button(root, canvas)
    root.mainloop()
