import os
import re
import datetime

MTempDict = {}

def ms_path(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                range
def date_validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

#TODO: Change os.listdir to scandir() function
def scanFolderFileExtensions(folderPath):
    MTempDict = {}
    for item in os.listdir(folderPath):
        if os.path.splitext(item)[1] == '.DNG':
            filePath = os.path.join(folderPath, item)
            fileDate = getModifiedDateFromFile(filePath)
            MTempDict[filePath] = fileDate
    return MTempDict
            
def createKaperFormatFolders(path):
    ms_path(os.path.join(path,'00_master'))
    ms_path(os.path.join(path,'01_gotowe'))
    ms_path(os.path.join(path,'02_postprodukcja'))
    return True

def createKaperDateFormat(path, createdDate):
    print("Próbuję stworzyć folder : " + os.path.join(path,createdDate)) 
    ms_path(os.path.join(path,createdDate))
    return createdDate

def createKaperDateAndFormatFolders(filePath, date):
    path = os.path.split(filePath)[0]
    #file = os.path.split(i)[1]
    createKaperDateFormat(path,date)
    createKaperFormatFolders(os.path.join(path,date))

def moveDNGFileToMasterFolder(filePath, DestinyPath):
    originPath = os.path.split(filePath)[0]
    fileName = os.path.split(filePath)[1]
    try:
        os.rename(filePath,os.path.join(DestinyPath, fileName))
    except WindowsError:
        raise WindowsError("I cannot rename/move file! Program error")
    
def getMasterFolderFromDatePath(datePath):
    return os.path.join(datePath, '00_master')

def checkIfFileIsDirectory(path, file):
    if os.path.isdir(os.path.join(path,file)):
        return True
    else:
        return False
    
def getModifiedDateFromFile(filePath):
    timestamp = os.path.getmtime(filePath)
    return datetime.datetime.fromtimestamp(timestamp).isoformat()[:10]

def prepareListdirPath(folder_path):
    if(folder_path.get() != ""):
        return os.listdir(folder_path.get())
    else:
        print("NIE WSKAZANO POPRAWNEJ ŚCIEŻKI PLIKU!")
        
def getPathFromTkVar(tk_var):
    if(tk_var.get() != ""):
        return tk_var.get()
    else:
        print("NIE WSKAZANO POPRAWNEJ ŚCIEŻKI PLIKU!")
    
def kaper_create_folders(tk_path_var,selectedMode):
    base_folder_structure = prepareListdirPath(tk_path_var)
    path = getPathFromTkVar(tk_path_var)
    print("Witaj w programie do przenoszenia plików (tymczasowo tylko DNG)")
    print("Plik programu powinien znajdować się w miejscu na ktorym bedziesz dokonywal operacji")
    if(selectedMode.get() == 1):
        advanvedMode= "y"
    elif(selectedMode.get() == 2):
        advanvedMode= "n"
    else:
        advanvedMode= "n"
    
    advanvedMode = advanvedMode.lower()
    if(advanvedMode[0]=="y"):
        for catalog in base_folder_structure:
            if checkIfFileIsDirectory(path, catalog):
                print(path + ". I am checking folder ...: " + catalog)
                MTempDict = scanFolderFileExtensions(os.path.join(path,catalog))
                #print(MTempDict)
                for key in MTempDict:
                    createKaperDateAndFormatFolders(key,MTempDict.get(key))
                    moveDNGFileToMasterFolder(key,os.path.join(path,catalog,MTempDict.get(key),'00_master'))
                print("Liczba przeniesionych plików : " + str(len(MTempDict)))
        print("Program zakończył działanie")
        
    elif (advanvedMode[0]=="e"):
        exit()
    else:
        MTempDict = scanFolderFileExtensions(path)
        for key in MTempDict:
            createKaperDateAndFormatFolders(key,MTempDict.get(key))
            moveDNGFileToMasterFolder(key,os.path.join(path,MTempDict.get(key),'00_master'))
        print("Liczba przeniesionych plików : " + str(len(MTempDict)))
    print("Program zakończył działanie")
        
def main(tk_path_var, selectedMode):
    kaper_create_folders(tk_path_var,selectedMode)
