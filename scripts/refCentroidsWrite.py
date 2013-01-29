import FITS
import darc

c=darc.Control("main")
refCen = c.Get("refCentroids")
print refCen.shape

#data = refCen.reshape(480,640)
#FITS.Write(data,'refCentroidsImage20130129.fits',writeMode='a')

