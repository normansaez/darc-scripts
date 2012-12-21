import numpy
import darc
d=darc.Control('main')
d.Set('dani',39.5)
bg=d.Get('bgImage')
stream=d.GetStream('mainrtcPxlBuf')#a single frame
#print stream
data=d.GetStreamBlock('mainrtcPxlBuf',100)#100 frames - as a list
for k,v in data.items():
	print k
	print v
print len(data['mainrtcPxlBuf'])
arrdata=numpy.array([x[0] for x in data])
data=d.SumData('rtcCentBuf',100)[0]
data/=100
#
##To take a background:
bg=d.SumData('rtcPxlBuf',100,'f')[0]/100
d.Set('bgImage',bg)
print type(bg)
##Note, you could also create a background using the camera calibration tool.
##Create ref slopes. 
#ref=d.SumData('rtcCentBuf',100)[0]/100 
#d.Set('refCentroids',ref)
##Create ref slopes. 
#ref=d.SumData('rtcCentBuf',100)[0]/100 
#d.Set('refCentroids',ref)
#
##To do some poking...: 
#nacts=d.Get('nacts') 
#nslopes=d.Get('subapFlag').sum()*2
#d.Set('addActuators',0)
##open the mirror library (if not already)
#d.Set('mirrorOpen',1)
#d.Set('closeLoop',0)
#pmx=numpy.zeros((nacts,nslopes),numpy.float32) 
#acts=numpy.ones((nacts,),numpy.float32)*32768
#r=5000
#n=10
