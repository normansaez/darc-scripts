#!/usr/bin/python           

import socket               
from BeagleDarc.Model import BeagleDarcServerM

class BeagleDarcClient:
    def __init__(self):
        self.bdsm = BeagleDarcServerM('beagledarc_server')

    def connect(self):
        s = socket.socket()         
        s.connect((self.bdsm.host, int(self.bdsm.port))) 
        s.send("M1:90:END")
        while True:
            response = s.recv(1024)
            print response
            if response.__contains__("ack"):
                s.close    
                break

if __name__ == '__main__':
    bdc = BeagleDarcClient()
    bdc.connect()
