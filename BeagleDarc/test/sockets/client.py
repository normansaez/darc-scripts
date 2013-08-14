#!/usr/bin/python           

import socket               

s = socket.socket()         
host = socket.gethostname() 
#host = '192.168.2.3'
port = 12345                
s.connect((host, port))
s.send("sended from client")
while 1:
    response = s.recv(1024)
    print response
    if response.__contains__("ack"):
        s.close    
        break
