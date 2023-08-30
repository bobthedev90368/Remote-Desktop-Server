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
usedports = []
connnections = []

def getnewport():
    global usedports
    if not usedports:
        lastport = portrange[0]
    else:
        lastport = usedports[-1] + 1
    while True:
        if not lastport in portblacklist and not lastport in usedports and not lastport > portrange[1]:
            usedports.append(lastport)
            return lastport
        elif lastport > portrange[1]:
            return 99999
        else:
            lastport += 1

def waitconnect(host, checkinport, cuemax):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initsocket:
        initsocket.bind((host, checkinport))
        initsocket.listen(cuemax)
        clientsocket, address = initsocket.accept()
        with clientsocket:
            print("Connected @", address)
            recieveddata = clientsocket.recv(checkinport)
            print(recieveddata)
            try:
                data = json.loads(recieveddata.decode("utf-8"))
                preshareencrypt = False
            except:
                preshareencrypt = True
                fernet = Fernet(presharedencryption)
                data = json.loads(fernet.decrypt(recieveddata).decode("utf-8"))
                print(data)
            if data['encrypt'] == True:
                port = getnewport()
                encryptiontoken = Fernet.generate_key()
                connnections.append({"port": port, "encryptiontoken": encryptiontoken, "presharedencryption": preshareencrypt, "refrence": data["refrence"]})
                toreturn = {'encryptiontoken': encryptiontoken, 'port': getnewport(), "id": len(connnections)-1}
            else:
                port = getnewport()
                connnections.append({"port": port, "encryptiontoken": False, "presharedencryption": preshareencrypt, "refrence": data["refrence"]})
                toreturn = {'port': getnewport(), "id": len(connnections)-1}
            print(toreturn)
            print(connnections)
waitconnect(host, checkinport, 5)