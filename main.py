import sys, Tkinter
sys.path.insert(0, "./gui/")
from button import OpenFolderButton, NextBatchButton
from config import *

# Note: need to set size for bg_canvas here; otherwise it will grow disregard the size set while created!
def AuxscrollFunction(event):
    bg_canvas.configure(scrollregion=bg_canvas.bbox("all"), height=THUMB_HEIGHT)

# create root
root = Tkinter.Tk()
root.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT)+"+100+100")
root.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
root.title("Find Duplicated Photos")

# create frame for selected photo display
selected_photo_frame = Tkinter.Frame(root, height=DISPLAY_HEIGHT)
selected_photo_frame.pack(fill=Tkinter.BOTH, expand=True)

# create background for scroll bar
bg_frame = Tkinter.Frame(root, height=THUMB_HEIGHT)
bg_frame.pack(fill=Tkinter.BOTH, expand=True)
bg_canvas = Tkinter.Canvas(bg_frame)
xscrollbar = Tkinter.Scrollbar(bg_frame, orient="horizontal", command=bg_canvas.xview)
xscrollbar.pack(side="bottom", fill="x")
xscrollbar.grid_forget()
bg_canvas.configure(xscrollcommand=xscrollbar.set)
bg_canvas.pack(fill=Tkinter.BOTH, expand=True)

# create frame for duplicated photo batch display
batch_photo_frame = Tkinter.Frame(bg_canvas, height=THUMB_HEIGHT)
bg_canvas.create_window((0,0),window=batch_photo_frame,anchor='nw')
batch_photo_frame.bind("<Configure>", AuxscrollFunction)
# Note: don't pack batch_photo_frame here, otherwise scroll bar won't show!!!

# create buttons
button1 = OpenFolderButton(root, batch_photo_frame)
button2 = NextBatchButton(root, batch_photo_frame, selected_photo_frame, button1)
root.mainloop()
