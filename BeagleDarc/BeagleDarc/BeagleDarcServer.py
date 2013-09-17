#!/usr/bin/python            

import socket                
import time
from BeagleDarc.Model import BeagleDarcServerM

class BeagleDarcServer:
    def __init__(self):
        self.bdsm = BeagleDarcServerM('beagledarc_server')

    def connect(self):
        s = socket.socket()          
        #host = socket.gethostname()  
        s.bind((self.bdsm.host, int(self.bdsm.port))) 
        s.listen(30) 
        count = 0
        #while True:
        c, addr = s.accept()    
        print 'Got connection from', addr
        c.send('Conection number: %d' %(count))
        msg = c.recv(1024)
        msg_ = msg.split(':')
        steps = int(msg_[1])
        for i in range(1,steps):
            c.send('%d' %(i))
            time.sleep(1)
        count += 1
        c.send('ack')
        c.close()

if __name__ == '__main__':
    bds = BeagleDarcServer()
    bds.connect()
