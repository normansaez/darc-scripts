import numpy
import controlCorba
import FITS

prefix = "main"
c=controlCorba.controlClient(prefix)
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
c.Set("refCentroids",raw_data)

#print "darcmagic set refCentroids -file=refslopes.fits"
