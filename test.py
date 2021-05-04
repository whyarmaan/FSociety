import readline
import os

def completer(text: str, state):
    text = text.split(" ")[-1]
    a = []
    for root, folders, files in os.walk("."):
        for folder in folders:
            if folder.startswith(text):
                a.append(folder)
        
        for file in files:
            if file.startswith(text):
                a.append(file)
    
    return a[state]

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")
input("Give Input: ")
