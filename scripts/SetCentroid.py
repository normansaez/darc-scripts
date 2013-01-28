import numpy
import controlCorba
d=controlCorba.controlClient("main")

slopes=d.Get("refCentroids")
print slopes
nslopes=d.Get("subapFlag").sum()*2
xxx=numpy.zeros((nslopes,),numpy.float32)
d.Set("refCentroids",xxx)


print "darcmagic set refCentroids -file=refslopes.fits"
