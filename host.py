import time
import json
import socket
import random
import string
from cryptography.fernet import Fernet

host = "127.0.0.1"
checkinport = 1024 #default "checkin" port
presharedencryption = b'ts1UOpWUIE-PFmHE-HWhVWKS5YPrfSQzHjwFm7wnCIQ=' #set to whatever PRESHARED encryption key
authcode = "" #add the password if you want to enable password authentication
portrange = [1025, 65536] #Excluding default checkin port lowest port at 0 value highest at 1
portblacklist = [] #any ports you dont want being used
usedports = []
connnections = []
defaultpassphraselength = 10 #passphrase used internally for making sure clients are authorized to connect higher = more secure


def generatepassphrase():
    passphrase = ""
    characters = string.ascii_letters + string.digits + string.punctuation
    for i in range(defaultpassphraselength):
        passphrase = passphrase + random.choice(characters)
    return passphrase


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

def clientlistner(host, port):
    print(host,port,connnections)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.bind((host, port))
        client.listen()
        clientsocket, address = client.accept()
        with clientsocket:
            print("Connected @", address)

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
                data = json.loads(Fernet(presharedencryption).decrypt(recieveddata).decode("utf-8"))
            print(data)
            passphrase = generatepassphrase()
            if data['encrypt'] == True:
                port = getnewport()
                encryptiontoken = Fernet.generate_key()
                connnections.append({"port": port, "encryptiontoken": encryptiontoken, "presharedencryption": preshareencrypt, "refrence": data["refrence"], "passphrase": passphrase})
                toreturn = {'encryptiontoken': encryptiontoken, 'port': getnewport(), "id": len(connnections)-1, "passphrase": passphrase}
            else:
                port = getnewport()
                connnections.append({"port": port, "encryptiontoken": False, "presharedencryption": preshareencrypt, "refrence": data["refrence"], "passphrase": passphrase})
                toreturn = {'port': getnewport(), "id": len(connnections)-1, "passphrase": passphrase}
            if presharedencryption:
                toreturn = Fernet(presharedencryption).encrypt(bytes(json.dumps(toreturn),encoding="utf-8"))
            else:
                toreturn = bytes(json.dumps(toreturn),encoding="utf-8")
            clientsocket.sendall(toreturn)
            print(toreturn)
            print(connnections)
            clientlistner(host, port)
            
waitconnect(host, checkinport, 5)