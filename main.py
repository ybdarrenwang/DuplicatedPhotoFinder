import sys, Tkinter
sys.path.insert(0, "./gui/")
import button
from config import *

# Note: need to set size for bg_canvas here; otherwise it will grow disregard the size set while created!
def AuxscrollFunction(event):
    bg_canvas.configure(scrollregion=bg_canvas.bbox("all"), height=THUMB_HEIGHT)

# create root
root = Tkinter.Tk()
root.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT)+"+100+100")
root.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
root.title("Find Duplicated Photos")

Tkinter.Grid.columnconfigure(root, 0, weight=0)
Tkinter.Grid.columnconfigure(root, 1, weight=0)
Tkinter.Grid.columnconfigure(root, 2, weight=1)
Tkinter.Grid.columnconfigure(root, 3, weight=0)
Tkinter.Grid.rowconfigure(root, 0, weight=1)
Tkinter.Grid.rowconfigure(root, 1, weight=1)
Tkinter.Grid.rowconfigure(root, 2, weight=0)

# create frame for selected photo display
selected_photo_frame = Tkinter.Frame(root, height=DISPLAY_HEIGHT, width=DISPLAY_WIDTH)
selected_photo_frame.grid(row=0, column=0, columnspan=3, sticky=Tkinter.W+Tkinter.E)

selected_photo_info_frame = Tkinter.Frame(root, height=DISPLAY_HEIGHT, width=INFO_WIDTH)
selected_photo_info_frame.grid(row=0, column=3, sticky=Tkinter.W+Tkinter.E)

# create background for scroll bar
bg_frame = Tkinter.Frame(root, height=THUMB_HEIGHT)
bg_frame.grid(row=1, column=0, columnspan=4, sticky=Tkinter.W+Tkinter.E)
bg_canvas = Tkinter.Canvas(bg_frame)
xscrollbar = Tkinter.Scrollbar(bg_frame, orient="horizontal", command=bg_canvas.xview)
xscrollbar.pack(side="bottom", fill="x")
xscrollbar.grid_forget()
bg_canvas.configure(xscrollcommand=xscrollbar.set)
bg_canvas.pack(fill=Tkinter.BOTH, expand=True, padx=5, pady=5)

# create frame for duplicated photo batch display
batch_photo_frame = Tkinter.Frame(bg_canvas, height=THUMB_HEIGHT)
bg_canvas.create_window((0,0),window=batch_photo_frame,anchor='nw')
batch_photo_frame.bind("<Configure>", AuxscrollFunction)
# Note: don't pack batch_photo_frame here, otherwise scroll bar won't show!!!

# create buttons
button_cfg = button.ConfigButton(root, 2, 3)
button_open = button.OpenFolderButton(root, batch_photo_frame, button_cfg.config, 2, 0)
button_next = button.NextBatchButton(root, batch_photo_frame, selected_photo_frame, button_open.photo_crawler, 2, 1)

root.mainloop()
