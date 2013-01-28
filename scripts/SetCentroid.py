import numpy
import controlCorba
import FITS

d=controlCorba.controlClient("main")

slopes=d.Get("refCentroids")
print slopes
nslopes=d.Get("subapFlag").sum()*2
print "---"
print d.Get("subapFlag").sum()
print "---"
#xxx=numpy.zeros((nslopes,),numpy.float32)
xxx=numpy.ones((nslopes,),numpy.float32)
#print xxx.shape
#print "lalalal"
#
#data = FITS.Read('r_centroid.fits')
#headers = data[0]
#xxx = data[1]
#
#print xxx
#print xxx.shape
#xxx = None
d.Set("refCentroids",xxx)
print "BEFORE SET ! "
slopes=d.Get("refCentroids")
print slopes

print "darcmagic set refCentroids -file=refslopes.fits"
