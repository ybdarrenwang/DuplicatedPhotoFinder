import sys, Tkinter
sys.path.insert(0, "./gui/")
from button import OpenFolderButton, NextBatchButton

#Tkinter.wantobjects = 0

#Need to set a max size for frameTwo. Otherwise, it will grow as needed, and scrollbar do not act
def AuxscrollFunction(event):
    bg_canvas.configure(scrollregion=bg_canvas.bbox("all"))#,width=1000,height=250)

# create root
root = Tkinter.Tk()
root.geometry("1000x300+100+100")
root.title("Find Duplicated Photos")

# create background for scroll bar
bg_frame=Tkinter.Frame(root)
bg_frame.pack(fill=Tkinter.BOTH, expand=True)
bg_canvas = Tkinter.Canvas(bg_frame)
xscrollbar = Tkinter.Scrollbar(bg_frame, orient="horizontal", command=bg_canvas.xview)
xscrollbar.pack(side="bottom", fill="x")
xscrollbar.grid_forget()
bg_canvas.configure(xscrollcommand=xscrollbar.set)
bg_canvas.pack(fill=Tkinter.BOTH, expand=True)

# create frame for photo canvas display
frame = Tkinter.Frame(bg_canvas)#, width=1000, height=250)
bg_canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>", AuxscrollFunction)
frame.focus_set()

# create buttons
button1 = OpenFolderButton(root, frame)
button2 = NextBatchButton(root, frame, button1)
root.mainloop()
