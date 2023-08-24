import time
import json
import socket
from cryptography.fernet import Fernet

host = "127.0.0.1"
checkinport = 1024 #default "checkin" port
presharedencryption = "" #set to whatever PRESHARED encryption key
authcode = "" #add the password if you want to enable password authentication

def waitconnect(host, checkinport, cuemax):
    initsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    initsocket.bind((host, checkinport))
    initsocket.listen(cuemax)

waitconnect(host, checkinport, 5)