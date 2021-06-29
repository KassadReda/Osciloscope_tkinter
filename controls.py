# -*- coding: utf-8 -*-
import json
import sys
from screen import Screen
from generator import Generator
major = sys.version_info.major
minor = sys.version_info.minor
if major == 2 and minor == 7:
    import Tkinter as tk
    from tkinter import *
    import tkFileDialog as filedialog
elif major == 3 and minor == 6:
    import tkinter as tk
    from tkinter import *
    from tkinter import filedialog
else:
    if __name__ == "__main__":
        print("Your python version is : ", major, minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import *
    from tkinter import filedialog



class Controller:
    def __init__(self, model, view, controllersList):
        self.model, self.view = model, view
        self.model.attach(self.view)
        #self.packing()
        controllersList.append(self)
        #if(self.view.canvas.bind("<Configure>", self.resize)) :
        #    print("presumably liking resize", self.model.name)
        self.view.addResizeCb(self.display_signal)
        #self.display_signal = False
        self.create_controls()
        


    def cb_update_magnitude(self, event):
        print("cb_update_magnitude(self,event)", self.mag_var.get())
        self.model.set_magnitude(self.mag_var.get())
        self.model.generate()
        self.display_signal()

    def cb_update_harmonics(self, event):
        print("cb_update_harmonics(self,event)",self.harmonics_var.get())
        self.model.set_harmonics(self.harmonics_var.get())
        self.model.generate()
        self.display_signal()

    def cb_update_phase(self, event):
        print("cb_update_harmonics(self,event)",self.phase_var.get())
        self.model.set_phase(self.phase_var.get())
        self.model.generate()
        self.display_signal()

    def cb_update_frequency(self, event):
        print("cb_update_harmonics(self,event)",self.freq_var.get())
        self.model.set_frequency(self.freq_var.get())
        self.model.generate()
        self.display_signal()

    def cb_activate_button(self):
        print("You selected the option " + str(self.radio_var.get()))
        self.model.harmo_odd_even = self.radio_var.get()
        self.display_signal()
        

    def create_controls(self):
        self.controllerFrame = tk.Frame(self.view.controlsFrame)
        self.mag_var = tk.DoubleVar()
        self.mag_var.set(self.model.get_magnitude())
        self.scale_mag = tk.Scale(self.controllerFrame, variable=self.mag_var,
                                  label="Amplitude",
                                  orient="horizontal", length=250,
                                  from_=0, to=1, relief="raised",
                                  sliderlength=20, resolution=0.1,
                                  tickinterval=0.5, command = self.cb_update_magnitude
                                  )

        self.harmonics_var = tk.IntVar()
        self.harmonics_var.set(self.model.get_harmonics())
        self.scale_harmonics = tk.Scale(self.controllerFrame, variable=self.harmonics_var,
                                        label="Harmonics",
                                        orient="horizontal", length=250,
                                        from_=1, to=50, relief="raised",
                                        sliderlength=20, tickinterval=5, command = self.cb_update_harmonics)

# phase + freq
        self.phase_var = tk.DoubleVar()
        self.phase_var.set(self.model.get_phase())
        self.scale_phase = tk.Scale(self.controllerFrame, variable=self.phase_var,
                                  label="Phase",
                                  orient="horizontal", length=250,
                                  from_=-180, to=180, relief="raised",
                                  sliderlength=20, resolution=0.1,
                                  tickinterval=0.5, command = self.cb_update_phase
                                  )

        self.freq_var = tk.DoubleVar()
        self.freq_var.set(self.model.get_frequency())
        self.scale_freq = tk.Scale(self.controllerFrame, variable=self.freq_var,
                                        label="Frequence",
                                        orient="horizontal", length=250,
                                        from_=1, to=50, relief="raised",
                                        sliderlength=20, tickinterval=5, command = self.cb_update_frequency)
        
# choose only odd harmonics or all harmonics
        self.harmonicsFrame = tk.LabelFrame(self.view.harmonicsFrame, text="Harmonics")
        self.radio_var = tk.IntVar()
        harmonics_btn = tk.Radiobutton(self.harmonicsFrame, text="All", variable=self.radio_var,
                             value=1, command=self.cb_activate_button)
        harmonics_btn.select()
        harmonics_btn.pack(anchor = "w")
        harmonics_btn = tk.Radiobutton(self.harmonicsFrame, text="Odd", variable=self.radio_var,
                             value=2, command=self.cb_activate_button)
        harmonics_btn.pack(anchor = "w")
        self.harmonicsFrame.pack(side = LEFT)

# display button
        self.displayFrame = tk.Frame(self.view.displayFrame)
        self.display_var = tk.IntVar()
        display_btn = tk.Checkbutton(self.displayFrame, text= self.model.name, variable=self.display_var,
                            command=self.display_signal)
        display_btn.select()
        display_btn.pack(anchor = "w")
        self.displayFrame.pack(side = LEFT)




    def update_sliders(self):
        self.mag_var.set(self.model.get_magnitude())
        self.harmonics_var.set(self.model.get_harmonics())
        self.phase_var.set(self.model.get_phase())
        self.freq_var.set(self.model.get_frequency())


    def display_signal(self) :
        if self.display_var.get() == 0 and len(self.view.canvas.find_withtag(self.model.name)) > 0 : 
            print("desapear !")
            self.view.canvas.delete(self.model.name)
        elif self.display_var.get() == 1 : 
            self.view.plot_signal(self.model.signal, self.model.name)



    
    def packing(self):
       
        #self.view.canvas.pack(expand=1, fill="both", padx=6)
        self.scale_mag.pack()
        self.scale_harmonics.pack()
        self.scale_freq.pack()
        self.scale_phase.pack()

    




