import numpy
import darc
import FITS

prefix = "main"
c=darc.Control(prefix)
fname="%ssubapLocation.fits" % prefix
##########################################
data=FITS.Read(fname)
subapLocation=data[1]
subflag=data[3]
c.Set("subapLocation",subapLocation,swap=1,check=1,copy=1)
print subflag
print subflag.shape
c.Set("subapFlag",subflag,swap=1)
print c.Get("subapFlag")
nslopes=c.Get("subapFlag").sum()*2
print nslopes
raw_data=numpy.ones((nslopes,),numpy.float32)
print c.Get("refCentroids")
print "---"
c.Set("refCentroids",raw_data)
print "---"
print c.Get("refCentroids")
print c.Get("nsub")
print c.Set("nsub",135)
print c.Get("nsub")
#print "darcmagic set refCentroids -file=refslopes.fits"
