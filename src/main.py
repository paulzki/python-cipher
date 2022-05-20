# SPDX-License-Identifier: GPL-3.0
from cryptography.fernet import Fernet
import os
import sys
import hashlib


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)       
    return allFiles  

def return_key(string):
    sha = hashlib.sha256()
    sha.update(string.encode('utf-8'))  
    return sha.hexdigest()[:41]+"_A="

def main():
    if len(sys.argv) > 2:
        key = return_key(sys.argv[2])
        fernet = Fernet(key)
        def encrypt(Buffer):
            encMessage = fernet.encrypt(Buffer)
            return encMessage

        def decrypt(Buffer):
            decMessage = fernet.decrypt(Buffer)
            return decMessage
            
        if sys.argv[1] == "-d":
            dirName = os.getcwd()
            listOfFiles = getListOfFiles(dirName)
            for file in listOfFiles:
                if file.endswith(".encrypted"):
                    with open(file,"rb") as f:
                        data = f.read()
                        encData = decrypt(data)
                        name = file.replace(".encrypted","")
                        
                        with open(name,"wb") as f:
                            f.write(encData)
                            print("Decrypted file: "+name)
                    os.remove(file)  
                        
        if sys.argv[1] == "-e":
            dirName = os.getcwd()
            listOfFiles = getListOfFiles(dirName)
            for file in listOfFiles:
                if file.endswith(".py"):
                    pass
                elif not file.endswith(".encrypted"):
                    with open(file,"rb") as f:
                        data = f.read()
                        encData = encrypt(data)      
                        with open(file+".encrypted","wb") as Enf:
                            Enf.write(encData) 
                            print("Encrypted: "+file)
                    os.remove(file)
    else:
        print("Usage: python main.py [func] [key]")
        exit()

if __name__ == "__main__":
    main()