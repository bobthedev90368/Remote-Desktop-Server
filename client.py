import time
import json
import socket
from cryptography.fernet import Fernet

host = "127.0.0.1"
checkinport = 1024 #default "checkin" port
encryption = False #An ecryption key will be generated in the handshake? [True/False]
presharedencryption = "" #set to whatever PRESHARED encryption key
authcode = "" #set if you have set password authentication on the host
refrences = "" #will set a text value in the client connection table