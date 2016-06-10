#!/usr/local/bin/python2.7
 
import Tkinter
from PIL import Image, ImageTk
 
root = Tkinter.Tk()
#some = Tkinter.Label(root, text="Tk's job!!", width="30", height="5")
#some.pack()
photo = "/Users/wasabi/Dropbox/Camera Uploads/2016-06-05 18.43.58.jpg"
_image = Image.open(photo).resize((250, 250), Image.ANTIALIAS)
_file = ImageTk.PhotoImage(_image)
 
_canvas1 = Tkinter.Canvas(root, width=250, height=250)
_canvas1.pack(side=Tkinter.LEFT)
_canvas1.create_image(0, 0, image = _file, anchor='nw')
 
_canvas2 = Tkinter.Canvas(root, width=250, height=250)
_canvas2.pack(side=Tkinter.LEFT)
_canvas2.create_image(0, 0, image = _file, anchor='nw')
 
root.mainloop()
