import tkinter.messagebox as tkMess
import os.path
from os import mkdir
from os import startfile
from shutil import copyfile
from shutil import copytree
from pathformats import *

def export(mod, out, mod_format, out_format):
    mod_path = mod + "/assets"
    out_path = out + "/assets"
    
    #print(mod_path)
    if not os.path.exists(mod_path):
        msg = "Error: Mod does not exist!"
        tkMess.showerror(title="Funkineer", message=msg)
        return
    if not os.path.exists(out): mkdir(out)
    if not os.path.exists(out_path): mkdir(out_path)
    
    do_bumpin = False
    
    for fn in filenames:
        old_path = formats[mod_format][fn]
        new_path = formats[out_format][fn]
        
        if fn == "bumpin": do_bumpin = True
        
        for file in files[fn]:
            #print(file, end=" : ")
            #print(mod_path + old_path, end=" : ")
            if os.path.exists(mod_path + old_path + file):
                tpath = out_path
                for p in new_path.split("/"):
                    tpath += "/" + p
                    if not os.path.exists(tpath): mkdir(tpath)
                #print(tpath)
                copyfile(mod_path + old_path + file,
                         out_path + new_path + file)
            #print("\n")
   
    if do_bumpin:
        if out_format == 2:
            old_path = formats[mod_format]["bumpin"]
            new_path = formats[2]["bumpin"]
            
            for file in files["bumpin"]:
                newfile = "KadeEngine" + file[:1].upper() + file[1:]
                copyfile(mod_path + old_path + file,
                         out_path + new_path + newfile)
                         
        if mod_format == 2:
            old_path = formats[2]["bumpin"]
            new_path = formats[out_format]["bumpin"]
            
            for file in files["bumpin"]:
                oldfile = "KadeEngine" + file[:1].upper() + file[1:]
                copyfile(mod_path + old_path + oldfile,
                         out_path + new_path + file)
   
    for mn in list(music[mod_format].keys()):
        old_path = music[mod_format][mn]
        new_path = music[out_format][mn]
        
        if os.path.exists(mod_path + old_path):
            tpath = out_path
            for p in new_path.split("/"):
                tpath += "/" + p
                if not os.path.exists(tpath): mkdir(tpath)
            copyfile(mod_path + old_path, out_path + new_path)
                            
    if os.path.exists(mod_path + "/data"):
        copytree(mod_path + "/data", out_path + "/data", dirs_exist_ok=True)
                            
    tkMess.showinfo(title="Funkineer", message="Conversion Complete!")
    os.startfile(out_path)
    