import socket
import json

host = "146.190.184.61"
port = 1024 #This will be the default call in port. The client or target will call into this port for a connection port
refrence = '1'
authcode = ''
encryption = False
encryptionkey = ''


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(json.dumps({'REQUEST':'recv', 'REFRENCE':refrence, 'AUTHCODE': authcode, 'ENCRYPTIONENABLE': encryption, 'ENCRYPTKEY': encryptionkey}).encode())
    data = json.loads(s.recv(1024).decode())
    print(data)

if data["STATUS"] == "GRANTED":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s2.connect((data["SERVER"], int(data["PORT"])))
        while True:
            data2 = s2.recv(data["PORT"])
            if data2:
                data2 = json.loads(data2.decode())
                print(data2)
            
elif data["STATUS"] == "ACCESS-DENIED":
    print("Access Denied")
elif data["STATUS"] == "DATA-MALFORMED":
    print("Data Bad")
else:
    print("A random error occured")