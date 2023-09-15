import time
import json
import socket
from cryptography.fernet import Fernet

host = "127.0.0.1"
checkinport = 1024 #default "checkin" port
encryption = False #An ecryption key will be generated in the handshake? [True/False]
presharedencryption = b'ts1UOpWUIE-PFmHE-HWhVWKS5YPrfSQzHjwFm7wnCIQ=' #set to whatever PRESHARED encryption key
authcode = "" #set if you have set password authentication on the host
refrence = "" #will set a text value in the client connection table

def connnect():
    if presharedencryption != "":
        fernet = Fernet(presharedencryption)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.connect((host, checkinport))
        if presharedencryption == "":
            serversocket.sendall(bytes(json.dumps({"refrence": refrence, "auth": authcode, "encrypt": encryption, "intergrity": True}),encoding="utf-8"))
        else:
            x = fernet.encrypt(bytes(json.dumps({"refrence": refrence, "auth": authcode, "encrypt": encryption, "intergrity": True}),encoding="utf-8"))
            print(x)
            serversocket.sendall(x)
        recieveddata = serversocket.recv(checkinport)
        print(recieveddata)
        try:
            data = json.loads(recieveddata.decode("utf-8"))
        except:
            data = json.loads(Fernet(presharedencryption).decrypt(recieveddata).decode("utf-8"))
        print(data)
connnect()