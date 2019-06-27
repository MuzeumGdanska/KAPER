#kaperCreationFolderRefactored.py

import os, re, datetime, ntpath
from tkinter import messagebox as mbox

MASTER_EXTENSIONS = ["dng","nef","raw","nrw","rw2","srw","srf","sr2","erf","ptx","pef","arw","crw","cr2"]
GOTOWE_EXTENSIONS = ["jpg","tiff","tif"]
POSTPRODUKCJA_EXTENSIONS = ["jpg","png","gif"]
        
def main(tk_path_var, selectedMode, createInvFoldersBool):
    #TODO: Po refaktoryzacji usunąć z aplikacji przesyłanie bool(createInvFoldersBool)
    kaper_files_distribute(tk_path_var,selectedMode)

#TODO rozdzielić funkcję na kilka funkcji : DRY
def kaper_files_distribute(tk_path_var,selectedMode):
    base_folder_structure = prepare_list_dir_path(tk_path_var)
    path = get_path_from_tkvar(tk_path_var)
#Tryb działania dla subfolderów
    if(selectedMode.get() == 1):
        advanced_mode= "multi"
#Tryb działania dla wskazanego folderu
    elif(selectedMode.get() == 2):
        advanced_mode= "single"
    else:
        advanced_mode= "error"
    ### SUBFOLDERS PROGRAM LOOP ###
    if(advanced_mode=="multi"):
        for catalog in base_folder_structure:
            if is_it_directory(path, catalog):
                singlepath = os.path.join(path, catalog)
                MTempDict = scan_folder_file_extensions(singlepath)
                relocate_format_files(MTempDict, singlepath)
            else:
                print(os.path.join(path,catalog), " nie jest katalogiem. Nie obejmuje zakres działania w trybie podfolderów.")
        ### SINGLE PROGRAM LOOP ###
    elif (advanced_mode == "single"):
        MTempDict = scan_folder_file_extensions(path)
        relocate_format_files(MTempDict, path)
    else:
        show_error("Brak trybu", "Nie wybrano zakresu folderów")
    show_info("Wykonano","Program zakończył działanie:")
    print("Program zakończył działanie.")

def relocate_format_files(format_files_list, path):
    MTempDict = format_files_list
    for key in MTempDict[0]:
        inventoryNumber = get_inv_from_kaper(key)
        create_kaper_inv_date_and_format_folders(key,MTempDict[0].get(key))
        move_file_to_destiny_path(key,os.path.join(path,inventoryNumber,MTempDict[0].get(key),'00_master'))
        ##TODO LOG IT  print("Liczba przeniesionych plików dng : " + str(len(MTempDict[0])))
    for key in MTempDict[1]:
        inventoryNumber = os.path.basename(key).split("_")[0]
        create_kaper_inv_date_and_format_folders(key,MTempDict[1].get(key))
        move_file_to_destiny_path(key,os.path.join(path,inventoryNumber,MTempDict[1].get(key),'01_gotowe'))
        ##TODO LOG IT  print("Liczba przeniesionych plików gotowe : " + str(len(MTempDict[1])))
    for key in MTempDict[2]:
        inventoryNumber = os.path.basename(key).split("_")[0]
        ##TODO LOG IT  #print("Ten numer " , inventoryNumber)
        create_kaper_inv_date_and_format_folders(key,MTempDict[2].get(key))
        move_file_to_destiny_path(key, os.path.join(path,inventoryNumber,MTempDict[2].get(key),'02_postprodukcja'))
        ##TODO LOG IT print("Liczba przeniesionych plików postprodukcja : " + str(len(MTempDict[2])))

def get_inv_from_kaper(file):
    inv_number = os.path.basename(file).split("_")[0]
    return inv_number

def show_error(error_title,string_message):
    mbox.showerror(error_title,string_message);

def show_info(info_title, string_message):
    mbox.showinfo(info_title,string_message)
    
def ms_path(path):
    if os.path.exists(path):
        return True
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                range
                print("Wystapił błąd 512 - nie można utworzyć folderu. Skontaktuj się z administratorem programu")

def date_validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    #TODO create LOG CLASS - informacje o błednych nazwach zapisywane do logów programu
def assign_fileextension_to_kaper_folder(file):
    try:
        ext = (os.path.splitext(file)[1]).replace(".","").lower()
        if ext in MASTER_EXTENSIONS:
            return "master"
        elif ext in GOTOWE_EXTENSIONS:
            return "gotowe"
        elif ext in POSTPRODUKCJA_EXTENSIONS:
            return "postprodukcja"
        else:
            print(file, " NIE UDAŁO SIĘ PRZYPORZĄDKOWAĆ!!!")
    except OSError as exception:
        show_error("Unexpected error:", sys.exc_info()[0])
        raise
        
#TODO: Change os.listdir to scandir() function
def scan_folder_file_extensions(folderPath):
    MTempDict = {}
    GTempDict = {}
    PTempDict = {}
    folder_scan_error = False
    for item in os.listdir(folderPath):
        if os.path.isdir(os.path.join(folderPath,item)) == False:
            filePath = os.path.join(folderPath, item)
            fileDate = get_modified_date_from_file(filePath)
            if(assign_fileextension_to_kaper_folder(item)) == "master":
                #TODO LOG IT print (item, " poleciał do katalogu master")
                MTempDict[filePath] = fileDate
            elif os.path.splitext(item)[0].endswith("p"):
                #TODO LOG IT print (item, " poleciał do katalogu postprodukcja w wyniku występowania symbolu P")
                PTempDict[filePath] = fileDate
            elif(assign_fileextension_to_kaper_folder(item)) == "postprodukcja":
                #TODO LOG IT print (item, " poleciał do katalogu postprodukcja")
                PTempDict[filePath] = fileDate
            elif(assign_fileextension_to_kaper_folder(item)) == "gotowe":
                #TODO LOG IT print (item, " poleciał do katalogu gotowe")
                GTempDict[filePath] = fileDate
            else:
                print(item , " należy sprawdzić, nie udało sie dopasowac do standardu, skontaktuj się z administratorem")
        else:
            #TODO LOG IT
            folder_scan_error = True
            #print (os.path.join(folderPath,item), " jest katalogiem. Obiekt nie będzie procedowany w iteracji.")
    if folder_scan_error:
        show_error("Błąd skanu folderu", "Prawdopodobnie w wybrany folderze roboczym występowały inne katalogi. Działanie programu ich nie obejmowało.")
    listOfDicts = [MTempDict, GTempDict,PTempDict]
    return listOfDicts

def create_kaper_inv_date_and_format_folders(filePath, date):
    inv_folder = ntpath.basename(filePath).split("_")[0]
    dir_name = ntpath.dirname(filePath)
    create_kaper_date_format(dir_name,inv_folder,date)
    create_kaper_format_folders(os.path.join(dir_name,inv_folder,date))
    
def create_kaper_date_format(path, inv_number, createdDate):
    kaper_inv_folder = os.path.join(path, inv_number)
    #TODO LOG IT : print(os.path.join(kaper_inv_folder,createdDate))
    ms_path(os.path.join(kaper_inv_folder,createdDate))
    return createdDate

def create_kaper_format_folders(path):
    #TODO LOG IT : print("Próbuję stworzyć foldery robocze w sciezce : " , path)
    ms_path(os.path.join(path,'00_master'))
    ms_path(os.path.join(path,'01_gotowe'))
    ms_path(os.path.join(path,'02_postprodukcja'))
    return True
    
def move_file_to_destiny_path(filePath, DestinyPath):
    originPath = os.path.split(filePath)[0]
    fileName = os.path.split(filePath)[1]
    countPath = os.path.join(DestinyPath, fileName)
    if len(countPath) > 254:
        print("Ostrzeżenie przed zbyt długa nazwą sciezki plików - powyżej 254 znaków")
    try:
        os.rename(filePath,os.path.join(DestinyPath, fileName))
    except WindowsError:
        raise WindowsError("I cannot rename/move file! Program error. Sprawdź nazwę ścieżki katalogu który wybrałeś.")

def is_it_directory(path, file):
    if os.path.isdir(os.path.join(path,file)):
        return True
    else:
        return False
    
def get_modified_date_from_file(filePath):
    timestamp = os.path.getmtime(filePath)
    return datetime.datetime.fromtimestamp(timestamp).isoformat()[:10]

def prepare_list_dir_path(folder_path):
    if(folder_path.get() != ""):
        return os.listdir(folder_path.get())
    else:
        show_error("Błąd ściezki pliku", "Nie wykazano poprawnej ściezki pliku. Sprawdz czy wybrałeś katalog  na których chcesz dokonać operacji")
        print("NIE WSKAZANO POPRAWNEJ ŚCIEŻKI PLIKU!")
        return False
        
def get_path_from_tkvar(tk_var):
    if(tk_var.get() != ""):
        return tk_var.get()
    else:
        print("NIE WSKAZANO POPRAWNEJ ŚCIEŻKI PLIKU!")


