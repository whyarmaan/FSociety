import socket

def PortScan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        return True
    except socket.error:
        return False

def GetBanner(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    s.connect((ip, port))
    s.send(b'GET HTTP/1.1 \r\n')
    ret = s.recv(1024).decode().rstrip()
    return ret
