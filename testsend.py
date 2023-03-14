import socket
import json
from cryptography.fernet import Fernet

host = "146.190.184.61"
port = 1024 #This will be the default call in port. The client or target will call into this port for a connection port
refrence = '1'
authcode = ''
encryption = False
encryptionkey = Fernet.generate_key()
fernet = Fernet(encryptionkey)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(json.dumps({'REQUEST':'trnsmt', 'REFRENCE':refrence, 'AUTHCODE': authcode, 'ENCRYPTIONENABLE': encryption, 'ENCRYPTKEY': encryptionkey.decode()}).encode())
    data = json.loads(s.recv(1024).decode())
    print(data)

if data["STATUS"] == "GRANTED":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        print(data["PORT"])
        s2.connect((data["SERVER"], data["PORT"]))
        print("Welcome to the Remote Desktop Client. \nHere are our commands.\nHelp - the help command.\nList - Lists availible connections")
        go = True
        while go:
            data2 = s2.recv(data["PORT"])
            if data2:
                if encryption:
                    data2 = json.loads(fernet.decrypt(data2).decode())
                elif not encryption:
                    data2 = json.loads(data2.decode())
                if 'STATUS' in data2:
                    pass
                elif data2["REQUEST"] == "CONNECTIONS-SEND":
                    print(data2)

            
            ui = input(">")
            if ui == "list":
                if encryption:
                    encMessage = fernet.encrypt(json.dumps({'REQUEST':'list', 'AUTHCODE': authcode}).encode())
                    s2.sendall(encMessage)
                elif not encryption:
                    s2.sendall(json.dumps({'REQUEST':'list', 'AUTHCODE': authcode}).encode())
                else:
                    pass
            elif ui == "help":
                pass
        while True:
            data2 = s2.recv(data["PORT"])
            if data2:
                data2 = json.loads(data2.decode())
                
elif data["STATUS"] == "ACCESS-DENIED":
    print("Access Denied")
elif data["STATUS"] == "DATA-MALFORMED":
    print("Data Bad")
else:
    print("A random error occured")