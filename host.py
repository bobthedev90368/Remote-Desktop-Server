import time, json, socket, random, string, threading, logging
from cryptography.fernet import Fernet

host = "127.0.0.1"
checkinport = 1024 #default "checkin" port
presharedencryption = b'ts1UOpWUIE-PFmHE-HWhVWKS5YPrfSQzHjwFm7wnCIQ=' #set to whatever PRESHARED encryption key
authcode = "" #add the password if you want to enable password authentication
portrange = [1025, 65536] #Excluding default checkin port lowest port at 0 value highest at 1
portblacklist = [] #any ports you dont want being used
usedports = []
connnections = []
defaultpassphraselength = 10 #passphrase used internally for making sure clients are authorized to connect. higher = more secure; too high = decryption issues


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

def clientlistner(id):
    logging.debug('Client listener - connection data: ' + json.dumps(connnections[id]))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.bind((connnections[id]['host'], connnections[id]['port']))
        client.listen()
        clientsocket, address = client.accept()
        with clientsocket:
            logging.info('Client listener - connnected: ' + str(address))
            while True:
                recieveddata = clientsocket.recv(connnections[id]['port']).decode("utf-8")
                if recieveddata != "":
                    logging.debug('Client listener - recieved data 1: ' + str(recieveddata))
                    if connnections[id]['presharedencryption']:
                        data = json.loads(Fernet(presharedencryption).decrypt(recieveddata).decode("utf-8"))
                    else: 
                        data = json.loads(recieveddata.decode("utf-8"))
                    logging.debug('Client listener - recieved data 2: ' + json.dumps(data))
                    break

def waitconnect(host, checkinport, cuemax):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initsocket:
        initsocket.bind((host, checkinport))
        initsocket.listen(cuemax)
        clientsocket, address = initsocket.accept()
        with clientsocket:
            logging.info('Client Initializer - connnected: ' + str(address))
            recieveddata = clientsocket.recv(checkinport)
            logging.debug('Client Initializer - recieved connection data 1: ' + str(recieveddata))
            try:
                data = json.loads(recieveddata.decode("utf-8"))
                preshareencrypt = False
            except:
                preshareencrypt = True
                data = json.loads(Fernet(presharedencryption).decrypt(recieveddata).decode("utf-8"))
            logging.debug('Client Initializer - recieved connection data 2: ' + json.dumps(data))
            if data['auth'] != authcode and authcode != "":
                clientsocket.close() 
                #restart the function
            else:
                passphrase = generatepassphrase()
                if data['encrypt'] == True:
                    port = getnewport()
                    encryptiontoken = Fernet.generate_key()
                    connnections.append({"port": port, "client": data["client"], "host": host, "encryptiontoken": encryptiontoken, "presharedencryption": preshareencrypt, "refrence": data["refrence"], "passphrase": passphrase})
                    toreturn = {'encryptiontoken': encryptiontoken, 'port': port, "host": host, "id": len(connnections)-1, "passphrase": passphrase}
                else:
                    port = getnewport()
                    connnections.append({"port": port, "client": data["client"], "host": host, "encryptiontoken": False, "presharedencryption": preshareencrypt, "refrence": data["refrence"], "passphrase": passphrase})
                    toreturn = {'port': port, "host": host, "id": len(connnections)-1, "passphrase": passphrase}
                logging.debug('Client Initializer - Sending connection data 1: ' + json.dumps(toreturn))
                if presharedencryption:
                    toreturn = Fernet(presharedencryption).encrypt(bytes(json.dumps(toreturn),encoding="utf-8"))
                else:
                    toreturn = bytes(json.dumps(toreturn),encoding="utf-8")
                logging.debug('Client Initializer - Sending connection data 2: ' + str(toreturn))
                clientsocket.sendall(toreturn)
                clientsocket.close()
                threading.Thread(target=clientlistner, args=(len(connnections)-1,)).start()

logging.basicConfig(filename=time.time(), format="%(asctime)s: %(message)s", level=logging.DEBUG, datefmt="%H:%M:%S")
waitconnect(host, checkinport, 5)