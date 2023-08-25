import time
import json
import socket
from cryptography.fernet import Fernet

host = "127.0.0.1"
checkinport = 1024 #default "checkin" port
presharedencryption = b'ts1UOpWUIE-PFmHE-HWhVWKS5YPrfSQzHjwFm7wnCIQ=' #set to whatever PRESHARED encryption key
authcode = "" #add the password if you want to enable password authentication
portrange = [1025, 65536] #Excluding default checkin port lowest port at 0 value highest at 1
portblacklist = [] #any ports you dont want being used

def waitconnect(host, checkinport, cuemax):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initsocket:
        initsocket.bind((host, checkinport))
        initsocket.listen(cuemax)
        clientsocket, address = initsocket.accept()
        with clientsocket:
            print("Connected @", address)
            while True:
                try:
                    try:
                        data = json.loads(clientsocket.recv(checkinport).decode("utf-8"))
                    except:
                        fernet = Fernet(presharedencryption)
                        data2 = clientsocket.recv(checkinport)
                        print(data2)
                        data = json.loads(fernet.decrypt(data2).decode("utf-8"))
                        break
                    print(data)
                except:
                    pass


waitconnect(host, checkinport, 5)