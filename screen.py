# -*- coding: utf-8 -*-

import sys
from observer import Observer
from generator import Generator
import json


major = sys.version_info.major
minor = sys.version_info.minor
if major == 2 and minor == 7:
    import Tkinter as tk
    import tkFileDialog as filedialog
    import tkMessageBox as msgBox
elif major == 3 and minor == 6:
    import tkinter as tk
    from tkinter import filedialog
    import tkinter.messagebox as msgBox
else:
    if __name__ == "__main__":
        print("Your python version is : ", major, minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog
    

# class Screen


class Screen(Observer):
    def __init__(self, parent, bg="white", name="signal"):
        Observer.__init__(self)
        self.parent = parent
        self.displayFrame = tk.LabelFrame(parent, text = "Display Menu")
        self.harmonicsFrame = tk.Frame(parent)
        self.controlsFrame = tk.Frame(parent)
        self.signal = []
        self.signals = {}
        self.name = name
        self.canvas = tk.Canvas(parent, bg=bg)
        self.width = int(self.canvas.cget("width"))
        self.height = int(self.canvas.cget("height"))
        self.tiles = 4
        #self.createMenu()
        self.resizeCb = []
        self.canvas.bind("<Configure>", self.resize)
        self.resize = False

    def get_signal(self):
        # signal=copy.copy(self.signal)
        return self.signal

    def get_canvas(self):
        return self.canvas

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_tiles(self):
        return self.tiles

    def set_tiles(self, tiles):
        self.tiles = tiles

    def create_grid(self):
        width, height = self.width, self.height
        tiles = self.tiles
        tile_x = width/tiles
        for t in range(1, tiles+1):          # lignes verticales
            x = t*tile_x
            self.canvas.create_line(x, 0, x, height, tags="grid")
            self.canvas.create_line(
                x, height/2-5, x, height/2+5, width=4, tags="grid")
        tile_y = height/tiles
        for t in range(1, tiles+1):        # lignes horizontales
            y = t*tile_y
            self.canvas.create_line(0, y, width, y, tags="grid")
            self.canvas.create_line(
                width/2-5, y, width/2+5, y, width=4, tags="grid")

    def delete(self):
        del self.signal[0:]
        self.notify()

    def plot_signal(self, signal, name="signal", color="red", erase=False, lissajou = False):
        width, height = self.width, self.height
        #print(signal)
        if signal and len(signal) > 1:
            self.canvas.delete(name)
            if lissajou :
                plot = [(x*width + width/2, y*height + height/2) for (x, y) in signal]
            else :
                plot = [(x*width, height/2*(y+1)) for (x, y) in signal]
            self.canvas.create_line(
                plot, fill=color, smooth=1, width=3, tags=name)
        
            

    def packing(self):
        self.displayFrame.pack()
        self.canvas.pack(expand=1, fill="both", padx=6)
        self.harmonicsFrame.pack()
        self.controlsFrame.pack()
        #self.scale_mag.pack()
        #self.scale_harmonics.pack()

    def update(self,subject=None) :
        print("update()",subject.get_name())
        if subject.get_name() not in self.signals.keys() : 
            self.signals[subject.get_name()] = subject.get_signal()
        else : 
            self.canvas.delete(subject.get_name())
        self.plot_signal(subject.get_signals(),subject.get_name())

    def addResizeCb(self, cb) :
        self.resizeCb.append(cb)

    def removeResizeCb(self, cb) :
        self.resizeCb.remove(cb)

    def resize(self, event):
        print("resizing")
        self.width = event.width
        self.height = event.height
        print("resize : ", self.width, self.height)
        self.canvas.delete("grid")
        self.create_grid()
        for cb in self.resizeCb :
            cb()


    


if __name__ == "__main__":
    root = tk.Tk()
    root.title("CAI Simulators")
    view = Screen(root)
    # view.generate()
    # view.set_tiles(tiles=10)
    view.create_grid()
    #view.plot_signal(view.get_signal(), view.get_name())
    view.packing()
    root.mainloop()
