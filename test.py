import readline
import os
import socket

def completer(text: str, state):
    text = text.split(" ")[-1]
    a = []
    for _, folders, files in os.walk("."):
        for folder in folders:
            if folder.startswith(text):
                a.append(folder)
        
        for file in files:
            if file.startswith(text):
                a.append(file)
    
    return a[state]

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def banner_grab():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 21))
    s.send(b'GET HTTP/1.1 \r\n')
    ret = s.recv(1024).decode().rstrip()
    print(ret)

banner_grab()