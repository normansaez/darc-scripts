import numpy
import darc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import controlCorba

#darcmagic get -name=subapLocation --prefix=main # Equivalente al codigo siguiente:
#darcmagic get -name=subapFlag --prefix=main
c=controlCorba.controlClient("main")
subapflag = c.Get("subapFlag")
#print subapflag
count = 1 
for i in range(0,len(subapflag)):
    if count == 11:
        print subapflag[i],
        count = 1
        print '\n',
    else:
        print subapflag[i],
        count = count + 1
subapLocation=c.Get("subapLocation")
print "\n#########################################"
#for i in range(0,121)
#    subapflag = 1
#print len(subapLocation)
#darcmagic get -name=bgImage --prefix=main
bg = c.Get("bgImage")
print "bg len %d " % len(bg)
#data = bg.reshape(640,480)
data = bg.reshape(480,640)
#plt.imshow(data)
#plt.gca().invert_yaxis()
#plt.show()

#subapLocation.shape=subapLocation.size/6,6
#subflag=c.Get("subapFlag")
#nsub=c.Get("nsub")
#npxlx=c.Get("npxlx")
#npxly=c.Get("npxly")
#print nsub
#print npxly
#print npxlx

