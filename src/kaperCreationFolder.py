import os
import re
import datetime
DATE_CREATED = ""

MasterTEMPArray = []
MTempDict = {}
GotoweTEMPArray = []
PostprodukcjaTEMPArray = []

#base_folder_structure = os.listdir('.')
#base_path = os.path.abspath('.')
#def scanFolderFileExtensions(listdir, filePaths = base_path):
        
def main(tk_path_var, selectedMode, createInvFoldersBool):
    # print(createInvFoldersBool.get()) #>>1/0
    createInvFoldersBool.set(1)
    if bool(createInvFoldersBool.get()) is False:
        kaper_create_folders(tk_path_var,selectedMode)
    if bool(createInvFoldersBool.get()) is True:
        invKaperCreateFolders(tk_path_var,selectedMode)
def testPrint():
    print("hello world")
    
def ms_path(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                range
                print("Wystapił błąd 212 - nie można utworzyć folderu. Skontaktuj się z administratorem programu")

def date_validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

#TODO: Change os.listdir to scandir() function
def scanFolderFileExtensions(folderPath):
    MTempDict = {}
    GTempDict = {}
    PTempDict = {}
    for item in os.listdir(folderPath):
        if os.path.splitext(item)[1] == '.DNG' or os.path.splitext(item)[1] == '.NEF':
            filePath = os.path.join(folderPath, item)
            fileDate = getModifiedDateFromFile(filePath)
            MTempDict[filePath] = fileDate
        elif os.path.splitext(item)[0].endswith("p"):
            #Logi ze skanu plików 
            #print(item, ': rozdzielone : ', os.path.splitext(item)[0],' and ', os.path.splitext(item)[1])
            filePath = os.path.join(folderPath, item)
            fileDate = getModifiedDateFromFile(filePath)
            PTempDict[filePath] = fileDate
        elif os.path.splitext(item)[1] == '.JPG' or os.path.splitext(item)[1] == '.jpg':
            filePath = os.path.join(folderPath, item)
            fileDate = getModifiedDateFromFile(filePath)
            GTempDict[filePath] = fileDate
        elif os.path.splitext(item)[1] == '.tiff' or os.path.splitext(item)[1] == '.TIFF' or os.path.splitext(item)[1] == '.tif' or os.path.splitext(item)[1] == '.TIF':
            filePath = os.path.join(folderPath, item)
            fileDate = getModifiedDateFromFile(filePath)
            GTempDict[filePath] = fileDate
            
    listOfDicts = [MTempDict, GTempDict,PTempDict]
    return listOfDicts
            
def createKaperFormatFolders(path):
    ms_path(os.path.join(path,'00_master'))
    ms_path(os.path.join(path,'01_gotowe'))
    ms_path(os.path.join(path,'02_postprodukcja'))
    return True

def createKaperDateFormat(path, createdDate):
    #print("Próbuję stworzyć folder : " + os.path.join(path,createdDate)) 
    ms_path(os.path.join(path,createdDate))
    return createdDate

def createKaperDateAndFormatFolders(filePath, date):
    path = os.path.split(filePath)[0]
    createKaperDateFormat(path,date)
    createKaperFormatFolders(os.path.join(path,date))
    
def createKaperInvNumberDateAndFormatFolders(filePath, date):
    path = filePath.split("_")[0]
    createKaperDateFormat(path,date)
    createKaperFormatFolders(os.path.join(path,date))
    
def moveFileToDestinyPath(filePath, DestinyPath):
    originPath = os.path.split(filePath)[0]
    fileName = os.path.split(filePath)[1]
    countPath = os.path.join(DestinyPath, fileName)
    if len(countPath) > 254:
        print("Ostrzeżenie przed zbyt długa nazwą sciezki plików - powyżej 254 znaków")
    try:
        os.rename(filePath,os.path.join(DestinyPath, fileName))
    except WindowsError:
        raise WindowsError("I cannot rename/move file! Program error. Sprawdź nazwę ścieżki katalogu który wybrałeś.")
    
def getMasterFolderFromDatePath(datePath):
    return os.path.join(datePath, '00_master')

def getGotoweFolderFromDatePath(datePath):
    return os.path.join(datePath, '01_gotowe')

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

def createInvNumberFromFile(file):
    kaperList = file.split('_')
    return kaperList[0]

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
                #MTempDict = scanFolderFileExtensions(os.path.join(path,catalog))
                listOfDicts = scanFolderFileExtensions(os.path.join(path,catalog))
                #print(MTempDict)
                for key in listOfDicts[0]:
                    createKaperDateAndFormatFolders(key,listOfDicts[0].get(key))
                    moveFileToDestinyPath(key,os.path.join(path,catalog,listOfDicts[0].get(key),'00_master'))
                print("Liczba przeniesionych plików : " + str(len(listOfDicts[0])))
                for key in listOfDicts[1]:
                    createKaperDateAndFormatFolders(key,listOfDicts[1].get(key))
                    moveFileToDestinyPath(key,os.path.join(path,catalog,listOfDicts[1].get(key),'01_gotowe'))
                print("Liczba przeniesionych plików : " + str(len(listOfDicts[1])))
                for key in listOfDicts[2]:
                    createKaperDateAndFormatFolders(key,listOfDicts[2].get(key))
                    moveFileToDestinyPath(key,os.path.join(path,catalog,listOfDicts[2].get(key),'02_postprodukcja'))
                print("Liczba przeniesionych plików : postprodukcja " + str(len(listOfDicts[2])))
        print("Program zakończył działanie")
        
    elif (advanvedMode[0]=="e"):
        exit()
    else:
        listOfDicts = scanFolderFileExtensions(path)
        for key in listOfDicts[0]:
            createKaperDateAndFormatFolders(key,listOfDicts[0].get(key))
            #moveFileToDestinyPath(key,os.path.join(path,listOfDicts[0].get(key),'00_master'))
        print("Liczba przeniesionych plików dng : " + str(len(listOfDicts[0])))
        for key in listOfDicts[1]:
            createKaperDateAndFormatFolders(key,listOfDicts[1].get(key))
            #moveFileToDestinyPath(key,os.path.join(path,listOfDicts[1].get(key),'01_gotowe'))
        print("Liczba przeniesionych plików gotowe : " + str(len(listOfDicts[1])))
        for key in listOfDicts[2]:
            createKaperDateAndFormatFolders(key,listOfDicts[2].get(key))
            #moveFileToDestinyPath(key,os.path.join(path,listOfDicts[2].get(key),'02_postprodukcja'))
        print("Liczba przeniesionych plików gotowe : postprodukcja" + str(len(listOfDicts[2])))
    print("Program zakończył działanie")


#TODO - Add Too Long Pathname Exception
def invKaperCreateFolders(tk_path_var,selectedMode):
    base_folder_structure = prepareListdirPath(tk_path_var)
    path = getPathFromTkVar(tk_path_var)
    print("Witaj w programie do przenoszenia plików")
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
                #MTempDict = scanFolderFileExtensions(os.path.join(path,catalog))
                listOfDicts = scanFolderFileExtensions(os.path.join(path,catalog))
                #print(MTempDict)
                for key in listOfDicts[0]:
                    inventoryNumber = os.path.basename(key).split("_")[0]
                    createKaperInvNumberDateAndFormatFolders(key,listOfDicts[0].get(key))
                    moveFileToDestinyPath(key,os.path.join(path,catalog,inventoryNumber,listOfDicts[0].get(key),'00_master'))
                print("Liczba przeniesionych plików : " + str(len(listOfDicts[0])))
                for key in listOfDicts[1]:
                    inventoryNumber = os.path.basename(key).split("_")[0]
                    createKaperInvNumberDateAndFormatFolders(key,listOfDicts[1].get(key))
                    moveFileToDestinyPath(key,os.path.join(path,catalog,inventoryNumber,listOfDicts[1].get(key),'01_gotowe'))
                print("Liczba przeniesionych plików : " + str(len(listOfDicts[1])))
                for key in listOfDicts[2]:
                    inventoryNumber = os.path.basename(key).split("_")[0]
                    createKaperInvNumberDateAndFormatFolders(key,listOfDicts[2].get(key))
                    moveFileToDestinyPath(key,os.path.join(path,catalog,inventoryNumber,listOfDicts[2].get(key),'02_postprodukcja'))
                print("Liczba przeniesionych plików : postprodukcja " + str(len(listOfDicts[2])))
        print("Program zakończył działanie")
        
    elif (advanvedMode[0]=="e"):
        exit()
    else:
        listOfDicts = scanFolderFileExtensions(path)
        for key in listOfDicts[0]:
            inventoryNumber = os.path.basename(key).split("_")[0]
            createKaperInvNumberDateAndFormatFolders(key,listOfDicts[0].get(key))
            moveFileToDestinyPath(key,os.path.join(path,inventoryNumber,listOfDicts[0].get(key),'00_master'))
        print("Liczba przeniesionych plików dng : " + str(len(listOfDicts[0])))
        for key in listOfDicts[1]:
            inventoryNumber = os.path.basename(key).split("_")[0]
            createKaperInvNumberDateAndFormatFolders(key,listOfDicts[1].get(key))
            moveFileToDestinyPath(key,os.path.join(path,inventoryNumber,listOfDicts[1].get(key),'01_gotowe'))
        print("Liczba przeniesionych plików gotowe : " + str(len(listOfDicts[1])))
        for key in listOfDicts[2]:
            inventoryNumber = os.path.basename(key).split("_")[0]
            #print("Ten numer " , inventoryNumber)
            createKaperInvNumberDateAndFormatFolders(key,listOfDicts[2].get(key))
            moveFileToDestinyPath(key, os.path.join(path,inventoryNumber,listOfDicts[2].get(key),'02_postprodukcja'))
        print("Liczba przeniesionych plików postprodukcja : " + str(len(listOfDicts[2])))
    print("Program zakończył działanie")

