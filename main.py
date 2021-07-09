import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkFile
import os.path
import fs
import sys

mod_verify = False
mod_location = ""
out_location = ""

versions = ["Funkin' Standard", "Kade Engine (1.0-1.4)", "Kade Engine (1.5+)"]
mod_format = versions[0]
out_format = versions[2]

class Hub(tk.Frame):
    def __init__(self, parent=None):
        super(Hub, self).__init__(parent)
        self.root = parent
        
        if getattr(sys, 'frozen', False):
            app_path = sys._MEIPASS
        elif __file__:
            app_path = os.path.dirname(__file__)
        self.root.iconbitmap(os.path.join(app_path, "icon.ico"))
        self.root.title("Funkineer - FNF Modding Tool")
        
        self.grid()
        
        window = tk.Frame(self.root)
        
        self.verify = ttk.Label(window, text="No Mod Found", foreground="#f00")
        
        self.iv    = tk.StringVar()
        ivf        = self.register(self.checkMod)
        self.input = tk.Entry(window, width=30, textvariable = self.iv,
                              validate="all", validatecommand=(ivf, "%P"))
                              
        self.invers = ttk.Combobox(window, values=versions, validate="all", validatecommand=self.update)
        self.outvers = ttk.Combobox(window, values=versions, validate="all", validatecommand=self.update)
        
        self.ov     = tk.StringVar()
        ovf         = self.register(self.checkOut)
        self.output = tk.Entry(window, width=30, textvariable = self.ov,
                               validate="all", validatecommand=(ovf, "%P"))
        
        self.finish = tk.Button(window, text="Convert", command=self.export)
        
        self.create_window(window)
    
    def export(self):
        mf = [i for i, v in enumerate(versions) if v == mod_format][0]
        of = [i for i, v in enumerate(versions) if v == out_format][0]
        print(mod_location, out_location, mf, of)
        fs.export(mod_location, out_location, mf, of)
    
    def checkOut(self, val=None):
        global out_location
    
        if val == None: loc = self.ov.get()
        else: loc = val
        out_location = loc
        return True
    
    def checkMod(self, val=None):
        global mod_location
        global mod_verify
    
        if val == None: loc = self.iv.get()
        else: loc = val
        
        #print(loc)
        
        mod_verify = True
        if not os.path.isdir(loc): mod_verify = False
        elif not os.path.isdir(loc + "/assets"): mod_verify = False
        self.verify.config(foreground="#090" if mod_verify else "#f00")
        self.verify.config(text="Mod Found" if mod_verify else "No Mod Found")
        
        mod_location = loc
        
        return True
        
    def openMod(self, dir=0):
        global mod_location
        global out_location
        
        loc = tkFile.askdirectory()
        if loc is not None: 
            if dir == 0:
                mod_location = loc
                self.iv.set(loc)
                self.checkMod()
            else:
                out_location = loc
                self.ov.set(loc)
        
    def update(self):
        global mod_format
        global out_format
        
        #print("up")
        mod_format = self.invers.get()
        out_format = self.outvers.get()
        #print(mod_format, out_format)
        self.finish.config(state=tk.DISABLED if mod_format == out_format else tk.NORMAL)
        return True
        
    def create_window(self, window):
        self.input.grid(padx=5, pady=2, column=0, columnspan=7, row=0, sticky='e')
        b_input = tk.Button(window, text="Open Folder", command=self.openMod)
        b_input.grid(padx=5, pady=2, column=0, columnspan=3, row=1, sticky='w')
        
        self.verify.grid(padx=5, pady=2, column=3, columnspan=4, row=1, sticky='ne')
        
        ttk.Separator(window, orient="horizontal").grid(padx=5, pady=7,
                                                        column=0, columnspan=7, row=2, sticky='we')
        
        ttk.Label(window, text="File Format - Input").grid(padx=7, pady=2,
                                                           column=0, columnspan=7, row=3, sticky='w')
        self.invers.set("Funkin' Standard")
        self.invers.state(["readonly"])
        self.invers.grid(padx=5, pady=2, column=0, columnspan=4, row=4, sticky=tk.W)
        
        ttk.Label(window, text="File Format - Output").grid(padx=7, pady=2,
                                                            column=0, columnspan=7, row=5, sticky='w')
        self.outvers.set("Kade Engine (1.5+)")
        self.outvers.state(["readonly"])
        self.outvers.grid(padx=5, pady=2, column=0, columnspan=4, row=6, sticky=tk.W)
        
        ttk.Separator(window, orient="horizontal").grid(padx=5, pady=7,
                                                        column=0, columnspan=7, row=7, sticky='we')
        
        ttk.Label(window, text="Destination Folder").grid(padx=7, pady=2,
                                                          column=0, columnspan=7, row=8, sticky='w')
                                                          
        self.output.grid(padx=5, pady=2, column=0, columnspan=7, row=9, sticky='w')
        b_output = tk.Button(window, text="Browse", command= lambda: self.openMod(1))
        b_output.grid(padx=5, pady=2, column=0, columnspan=2, row=10, sticky='w')
        self.finish.grid(padx=5, pady=2, column=2, columnspan=5, row=10, sticky='e')
        
        window.grid()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    window = Hub(parent=root)
    window.mainloop()