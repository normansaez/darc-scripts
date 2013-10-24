import FITS
import darc

#Takes camera instance
d=darc.Control('main')
#takes camera pixels (x,y)
pxlx =d.Get("npxlx")[0]
pxly =d.Get("npxly")[0]

#Set exposure time to zero:
d.Set("ManualExposureTimerRaw",0)
dark_to_take =  1000

exptime = d.Get('ManualExposureTimerRaw')
print "Exposure Time %s" % str(exptime)

for i in range(0, dark_to_take+1):
    #Preparing name for fits:
    if i == 0:
        fitsname = "bias_%s.fits" % str(i).zfill(3)
    else:
        exptime += 10
        fitsname = "dark_%s.fits" % str(i).zfill(3)
    print "Taking %s ...." % fitsname
    d.Set("ManualExposureTimerRaw",exptime)
    print "Exposure Time for %s is : %s" % (fitsname, str(exptime))
    #Getting image from buffer
    bg=d.SumData('rtcPxlBuf',1,'f')[0]/1
    #change the default shape of image (default shape is usually: (x*y,1))
    data = bg.reshape(pxlx,pxly)
    #writes a fits
    FITS.Write(data, fitsname, writeMode='a')
    print "done ...\n"
    if exptime >= 400:
        break

