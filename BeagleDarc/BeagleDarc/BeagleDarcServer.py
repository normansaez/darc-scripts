#!/usr/bin/python            

class BeagleDarcServer:
    def __init__(self):
        pass

#import socket                
#import time
#s = socket.socket()          
#host = socket.gethostname()  
#port = 12345                 
#s.bind((host, port))
#
#s.listen(5) 
#count = 0
#while True:
#    c, addr = s.accept()    
#    print 'Got connection from', addr
#    x = 0
#    c.send('Thank you for connecting: %d' %(count))
#    print c.recv(1024)
#    while x <= count:
#        time.sleep(0.01)
#        print "sleeping %d" % x
#        x += 1
#        c.send('---> %d' %(x))
#    count += 1
#    c.send('ack')
#    c.close() 
