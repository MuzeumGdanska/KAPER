#KAPERTOOLS-Agatex Hubert Kotarski, Muzeum Gdańsk ###
#Many Frames App
#License: CC BY 3.0 PL
import tkinter as tk                
from tkinter import font  as tkfont
from tkinter import filedialog
import os, time, sys
import kaperCreationFolder as kcf
GBoolMode = 0

class KaperApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        GPathVar = tk.StringVar()
        self.GPathVar = GPathVar
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        #Logo = resource_path("mg-logo.png")
        self.logo_img = os.path.join(os.path.abspath("."),"mg-logo.png")
        self.img= tk.PhotoImage(file=self.logo_img)
        self.logoLabel = tk.Label(self, image=self.img)
        self.logoLabel.pack()
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.minsize(800,500)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo,PageThree):
                    page_name = F.__name__
                    frame = F(parent=container, controller=self)
                    self.frames[page_name] = frame

                    # put all of the pages in the same location;
                    # the one on the top of the stacking order
                    # will be the one that is visible.
                    frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")

    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
        self.setGlobalPathVar(filename)
        
        
    def show_frame(self, page_name,*args):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def mainTest(self):
        print("This is main test function")

    def setGlobalPathVar(self, setVariable):
        global GPathVar
        self.GPathVar.set(setVariable)
        
    def getGlobalPathVar(self):
        return self.GPathVar

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="KAPER TOOLS APP 0.93", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        b1 = tk.Button(self, text="Standaryzacja plików KAPER",background='#d7d7d7',
                            command=lambda: controller.show_frame("PageOne"))
        b2 = tk.Button(self, text="Rozmieszczanie plików po katalogach",
                            command=lambda: controller.show_frame("PageTwo"))
        b3 = tk.Button(self, text="Nadpisywanie danych EXIF",background='#d7d7d7',
                            command=lambda: controller.show_frame("PageThree"))
        b4 = tk.Button(self, text = "Print global var",
                        command=lambda: print(controller.getGlobalPathVar()))
       # exitB = tk.Button(self, text = "Zamknij program",command= exit)
        
        b1.config(height = 10,width = 10)
        b2.config(height = 10,width = 10)
        b3.config(height = 5)
        b4.config(height = 20)
        b1.pack(fill = "x")
        b2.pack(fill = "x")
        b3.pack(fill = "x")
        #b4.pack(fill = "x")
        #exitB.config(height = 5)
        #exitB.pack(fill ="x")

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="FUNKCJA JESZCZE NIEDOSTĘPNA", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Powrót do strony głównej",
                           command=lambda: controller.show_frame("StartPage"),height=10)
        button.pack(side="bottom",fill="x")
        b2 = tk.Button(self, text="Wygeneruj nazwę zgodną ze standardem KAPER", state = 'disable',
                       command=lambda:kcf.testPrint())
        b2.pack()

class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        createInvFoldersBool = tk.IntVar()
        self.createInvFoldersBool = createInvFoldersBool
        subfolderRadio = tk.IntVar()
        self.subfolderRadio = subfolderRadio
    
        label = tk.Label(self, text="Wybór ściezki Kaper", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        bu2 = tk.Button(self,text="Wybierz katalog roboczy", command=lambda:controller.browse_button())
        bu2.config(height = 4)
        bu2.pack(fill="x")
        tk_path_var = controller.getGlobalPathVar()
        checkboxKaperInvFolder = tk.Checkbutton(self, text = "Tworzy nadrzędny folder z numerem inwentarzowym",
                                             variable = self.createInvFoldersBool, state = 'disable')
        
#Disable option with not creating inventory Number - old function is broken        
##      checkboxKaperInvFolder = tk.Checkbutton(self, text = "Create inventory number folder for every item",
##                                            variable = self.createInvFoldersBool)
        checkboxKaperInvFolder.pack();

        radioOne = tk.Radiobutton(self, text="Tylko dla wybranego folderu", variable=self.subfolderRadio, value=2,height=5,background='#d7d7d7')
        radioOne.pack(fill="both")

        radioGroup = tk.Radiobutton(self, text="Dla podfolderów w wybranym folderze",variable=self.subfolderRadio,  value=1,height=5,background='#d7d7d7')
        radioGroup.pack(fill="both")
        
        PathLabel = tk.Label(self, textvariable = controller.getGlobalPathVar().get())
        PathLabel.pack(side="top", fill="x", pady=10)
        self.PathLabel = PathLabel

        submitB = tk.Button(self,text="Uruchom rozmieszczanie po katalogach",
                         command= lambda: kcf.main(controller.getGlobalPathVar(),
                                                   self.subfolderRadio,
                                                   self.createInvFoldersBool))
        submitB.config(height = 4)
        submitB.pack(fill="both")
        
        button = tk.Button(self, text="Powrót do strony głównej",
                           command=lambda: controller.show_frame("StartPage"),height=10)
        button.pack(side="bottom",fill="x")
        

        self.update_GlobalPathLabel()

    # Function updates Path Label            
    def update_GlobalPathLabel(self):
        updatedPath = self.controller.getGlobalPathVar().get()
        self.PathLabel.configure(text=updatedPath)
        self.after(1000, self.update_GlobalPathLabel)
        
    def getPath(self):
        updatedPath = self.controller.getGlobalPathVar()
        return updatedPath
    
    #Helper function for kcf module - getting value of StringVar
    def changeStringToStringVar(self, string):
        strVar = tk.StringVar()
        strVar.set(string)
        return strVar
            
        
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Funkcja jeszcze niedostępna", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Powrót do strony głównej",
                           command=lambda: controller.show_frame("StartPage"),height=10)
        button.pack(side="bottom",fill="x")      
    
    
if __name__ == "__main__":
    app = KaperApp()
    app.mainloop()
    #while True:
     #   app.update_idletasks()
      #  app.update()
