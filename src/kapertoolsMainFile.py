#KAPERTOOLS-Agatex Hubert Kotarski Muzeum Gdansk Copyright ###
### MIT LICENSE ###
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os
import kaperCreationFolder as kcf

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global tk_path_var
    filename = filedialog.askdirectory()
    tk_path_var.set(filename)
    print(filename)
    
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Logo = resource_path("mg-logo.png")
root = Tk()
root.title("Muzeum Gdansk - Kaper Tools v.1.2")
root.minsize(800, 500)
v = IntVar()
createInvFoldersBool = IntVar()
tk_path_var = StringVar()
logo_img = os.path.join(os.path.abspath("."),"mg-logo.png")
img= tk.PhotoImage(file=logo_img)
logoLabel = tk.Label(root, image=img)
logoLabel.pack()


lbl1 = Label(master=root,textvariable=tk_path_var)
lbl1.pack(fill="both")
button2 = Button(text="Choose directory", command=browse_button,height=7)
button2.pack(fill="both")

checkboxKaperInvFolder = Checkbutton(root, text="Create inventory number folder for every item", variable=createInvFoldersBool).pack(fill="both")
radioOne = Radiobutton(root, text="For a selected folder only", variable=v, value=2,height=5,background='#d7d7d7').pack(fill="both")
radioGroup = Radiobutton(root, text="For subfolders in a group folder",variable=v,  value=1,height=5,background='#d7d7d7').pack(fill="both")
button3 = Button(text="Proceed kaper creation", command= lambda: kcf.main(tk_path_var,v,createInvFoldersBool),height=10)
button3.pack(fill="both")


mainloop()

