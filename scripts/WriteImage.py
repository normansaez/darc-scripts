import FITS
import darc
import time
import numpy

########## congiguration####
cameraName = "SH"
pxlx = 1920
pxly = 1080
#############################
c=darc.Control(cameraName)
stream=c.GetStream(cameraName+'rtcPxlBuf')#a single frame
#print stream
data=c.GetStreamBlock(cameraName+'rtcPxlBuf',100)#100 frames - as a list
arrdata=numpy.array([x[0] for x in data])
data=c.SumData('rtcCentBuf',100)[0]
data/=100
bg=c.SumData('rtcPxlBuf',100,'f')[0]/100
c.Set('bgImage',bg)
bg = c.Get("bgImage")
imageName = 'image_' + str(time.strftime("%Y_%m_%dT%H_%M_%S.fits", time.gmtime()))
print imageName
if bg == None:
    print "It seems that bg image is not set correctly (None)"
    exit(-1)
data = bg.reshape(pxly,pxlx)
FITS.Write(data, imageName, writeMode='a')

