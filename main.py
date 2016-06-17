import sys, Tkinter
sys.path.insert(0, "./gui/")
from button import OpenFolderButton, NextBatchButton

#Tkinter.wantobjects = 0

#Need to set a max size for frameTwo. Otherwise, it will grow as needed, and scrollbar do not act
def AuxscrollFunction(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"),width=1000,height=250)

if __name__=="__main__":
    root = Tkinter.Tk()
    root.geometry("1000x300+100+100")
    root.title("Find Duplicated Photos")
    bg_canvas = Tkinter.Canvas(root, width=1000, height=250)
    bg_canvas.pack(fill=Tkinter.BOTH, expand=True)
    frame = Tkinter.Frame(bg_canvas, relief=Tkinter.RAISED, borderwidth=1)
    scrollbar = Tkinter.Scrollbar(frame, orient="horizontal", command=bg_canvas.xview)
    scrollbar.grid(row=1, column=1, sticky='nsew')
    bg_canvas.configure(xscrollcommand=scrollbar.set)
    bg_canvas.configure(scrollregion=bg_canvas.bbox("all"),width=1000,height=250)
    frame.bind("<Configure>", AuxscrollFunction(bg_canvas))
    #scrollbar.pack(side="bottom", fill="y")
    #scrollbar.grid_forget()
    frame.pack(fill=Tkinter.BOTH, expand=True)
    bg_canvas.pack(fill=Tkinter.BOTH, expand=True)
    button1 = OpenFolderButton(root, frame)
    button2 = NextBatchButton(root, frame, button1)
    root.mainloop()
