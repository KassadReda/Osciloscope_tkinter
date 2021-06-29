from screen import Screen
from generator import Generator
from generator import Lissajou
from controls import Controller
import PIL.Image
import sys
major = sys.version_info.major
minor = sys.version_info.minor
if major == 2 and minor == 7:
    from Tkinter import *
    import Tkinter as tk
    import tkFileDialog as filedialog
    import tkMessageBox as msgBox
elif major == 3 and minor == 6:
    import tkinter as tk
    from tkinter import *
    from tkinter import filedialog
    import tkinter.messagebox as msgBox
else:
    if __name__ == "__main__":
        print("Your python version is : ", major, minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import *
    from tkinter import filedialog
    import tkinter.messagebox as msgBox

import json


class Launcher :

    def __init__(self,parent):
        self.parent=parent
        self.parent.title("CAI Simulators")
        self.controllersList = []
        self.view = Screen(parent)
        self.signal1 = Generator(mag=0.2,color="red", name="signal1")
        self.signal2 = Generator(mag=0.5,freq=5.0, name="signal2",color="green")
        self.signal1.generate()
        self.signal2.generate()
        self.controler1 = Controller(self.signal1, self.view, self.controllersList)
        self.controler2 = Controller(self.signal2, self.view, self.controllersList)
        self.view.set_tiles(tiles=10)
        self.view.create_grid()
        self.global_packing()
        self.createMenu()
        self.parent.mainloop()

    # pack all features at once
    def global_packing(self):
        for controller in self.controllersList:
            controller.view.packing()
            controller.controllerFrame.pack(side = LEFT)
            controller.packing()
    
    def createMenu(self):
        menubar = tk.Menu(self.parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open",command=self.openFile)
        filemenu.add_command(label="Save",command=self.saveFile)
        filemenu.add_command(label="Save Image",command = self.saveImage)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)

        viewMenu = tk.Menu(menubar, tearoff=0)
        viewMenu.add_command(label="Show Lissajou", command = self.showLissajou)

        helpMenu = tk.Menu(menubar, tearoff=0)
        helpMenu.add_command(label="About Us", command=self.aboutUs)
        helpMenu.add_command(label="About Tk", command=self.aboutTk)
        helpMenu.add_command(label="About Python", command=self.aboutPython)

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="View", menu=viewMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)

        self.parent.configure(menu=menubar)

    def aboutUs(self):
        msgBox.showinfo("About US","This software is created by : \n - KASSAD Reda : \t r7kassad@enib.fr  \n - MARCHESE Caroline : \t c7marche@enib.fr ")

    def aboutTk(self):
        msgBox.showinfo("About TkInter", "This Human Machine Interace was developed with TkInter, a Python API")

    def aboutPython(self):
        msgBox.showinfo("About Python", "This Human Machine Intrface was developed with Python 3.8")
    
    def exit(self) :
        if msgBox.askyesno("Exit","are you sure you want to exit?"):
            self.parent.destroy()

    def openFile(self):
        mesFormats = [ ('Texte','*.json')]
        nomFichier = filedialog.askopenfilename(parent=self.parent,filetypes=mesFormats,title="Ouvrire un signal")
        if len(nomFichier) > 0:
            print("open file  dans %s" % nomFichier)
                #Read JSON data into the datastore variable
        if nomFichier:
            print(nomFichier)
            with open(nomFichier, 'r') as f:
                datastore = json.load(f)
            for signal in datastore["signal"] :
                if signal['name']=="1" :
                    self.signal1.set_phase(signal["phase"])
                    self.signal1.set_frequency(signal["frequency"])
                    self.signal1.set_magnitude(signal["magnitude"])
                    self.signal1.set_harmonics(signal["harmonics"])
                    self.signal1.generate()
        
                elif signal['name']=="2" :
                    self.signal2.set_phase(signal["phase"])
                    self.signal2.set_frequency(signal["frequency"])
                    self.signal2.set_magnitude(signal["magnitude"])
                    self.signal2.set_harmonics(signal["harmonics"])
                    self.signal2.generate()

            for controller in self.controllersList :
                controller.update_sliders()
                controller.view.plot_signal(controller.model.signal, controller.model.name)


            
    def saveFile(self):
        mesFormats = [ ('Texte','*.json')
               ]
        nomFichier = filedialog.asksaveasfilename(parent=self.parent,filetypes=mesFormats,title="Sauvegardez le signal sous...")
        if nomFichier:
            print("Sauvegarde en cours dans %s" % nomFichier)
               # Writing JSON data
            with open(nomFichier, 'w') as f:
                signalX={'frequency': self.signal1.get_frequency(),
                     'magnitude': self.signal1.get_magnitude(),
                     'phase': self.signal1.get_phase(),
                     'harmonics': self.signal1.get_harmonics(),
                     'name':"1",'color':"red"}
                signalY={'frequency': self.signal2.get_frequency(),
                     'magnitude': self.signal2.get_magnitude(),
                     'phase': self.signal2.get_phase(),
                     'harmonics': self.signal2.get_harmonics(),
                        'name':"2",'color':"green"}
                signals=[]
                signals.append(signalX)
                signals.append(signalY)
                datastore = {'signal': signals}
                json.dump(datastore, f)   


    def saveImage(self):

        print("do it save")
        mesFormats = [('PNG', '*.png'),
                      ('JPG', '*.jpg'),
                      ('JPEG', '*.jpeg')]
        nomFichier = filedialog.asksaveasfilename(parent=self.parent,filetypes=mesFormats,title="Sauvegardez le signal sous...")
        if nomFichier :
            print("Sauvegarde en cours dans %s" % nomFichier)
            self.view.canvas.postscript(file = "buffer.eps")
            img = PIL.Image.open("buffer.eps")
            img.save(nomFichier)

    def showLissajou(self):
        self.top=tk.Toplevel(self.parent)
        self.top.resizable(0,0)
        self.top.title("Lissajou")
        self.lissajou=Screen(self.top)
        self.lissajou.create_grid()
        self.signal_1_2=Lissajou("X-Y",self.signal1.get_signal(),self.signal2.get_signal(),"blue")
        self.signal_1_2.attach(self.lissajou)
        self.lissajou.plot_signal(self.signal_1_2.signal, self.signal_1_2.name, lissajou=True)
        self.lissajou.packing()
            




root = tk.Tk()
root.minsize(500, 700)
Launcher(root)