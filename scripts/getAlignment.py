import FITS
import numpy
import matplotlib.pyplot as plt
import controlCorba

#darcmagic get -name=subapLocation --prefix=main
#darcmagic get -name=subapFlag --prefix=main
#darcmagic get -name=bgImage --prefix=main
initial = numpy.zeros((15,15), numpy.int32)
print "################"
print initial
print "################"
initial = initial.reshape(225)
print initial
print "################"
c=controlCorba.controlClient("main")
subapflag = c.Get("subapFlag")
print subapflag
print type(subapflag)
print subapflag.dtype
c.Set("subapFlag",initial,com="",swap=1,check=1,copy=1)
print "########### despues del set ##"
subapflag = c.Get("subapFlag")
print "----------------"
pxl = c.Get("pxlCnt")
print pxl
print type(pxl)
print pxl.size
print pxl.shape
print pxl.reshape(11,11)
print "----------------"
count = 1 
for i in range(0,len(subapflag)):
    if count == 11:
        print subapflag[i],
        count = 1
        print '\n',
    else:
        print subapflag[i],
        count = count + 1
sf = subapflag.reshape(11,11)
print "\n#########################################"
print sf
#subapLocation=c.Get("subapLocation")
#subapLocation.shape=subapLocation.size/6,6
#subflag=c.Get("subapFlag")
#nsub=c.Get("nsub")
#npxlx=c.Get("npxlx")
#npxly=c.Get("npxly")
#print nsub
#print npxly
#print npxlx
print "\n#########################################"
bg = c.Get("bgImage")
print "bg len %d  480*640 = %d" % (len(bg),480*640)
#data = bg.reshape(640,480)
FITS.Write(bg,'myfitsBG.fits')
data = bg.reshape(480,640)
print data
#plt.imshow(data)
#plt.gca().invert_yaxis()
#plt.show()
FITS.Write(data,'myfits.fits')

