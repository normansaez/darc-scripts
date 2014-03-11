# coding: utf-8
import numpy
import gtk
import darc
import FITS
import correlation
import calibrate
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import pylab
import FITS
import matplotlib.pyplot as plt
import pylab

def makeIdent(npxlx=None,npxly=None,sl=None):
    d=darc.Control("SH")
    npxly = numpy.zeros((ncam,), numpy.int32)#An array of length ncam, specifying the number of pixels in a vertical direction with an entry for each frame grabber.
    npxly[:] = 1080#An array of length ncam, specifying the number of pixels in a vertical direction with an entry for each frame grabber.
    npxlx = npxly.copy()#An array of length ncam, specifying the number of pixels in a horizontal direction with an entry for each frame grabber.
    npxlx[:] = 1920#An array of length ncam, specifying the number of pixels in a horizontal direction with an entry for each frame grabber.
    nsub = nsubx*nsuby #An array with ncam entries, specifying the number of sub-apertures for each frame grabber.
    sf=d.Get("subapFlag")
    if npxlx==None:
        npxlx=d.Get("npxlx")
    if npxly==None:
        npxly=d.Get("npxly")
    if sl==None:
        sl=d.Get("subapLocation")
    ident=correlation.generateIdentityCorr(npxlx,npxly,nsub,sf,sl)
    return ident
def getSlopes(img,pad=0,retcorr=0):
    """Computes slopes if img is used as a correlation image"""
    d=darc.Control("SH")
    cm=d.Get("centroidMode")
    if type(cm)==numpy.ndarray and numpy.any(cm[-49:]):#in correlation mode.
        cur=getCurrentImg()
        usenow=1
    else:
        cur=makeIdent()
        usenow=0
    sf=d.Get("subapFlag")
    nsub=d.Get("nsub")
    corr=correlation.makeCorrelation(img,cur,1,d.Get("npxlx"),d.Get("npxly"),nsub,d.Get("subapLocation"),sf,pad)
#def makeCorrelation(psf,img,ncam,npxlx,npxly,nsub,subapLocation,subflag,pad=None,savespace=0):
#    """Correlates 2 images with optional padding"""
    slopes=calibrate.makeSlopes(corr["correlation"],1,nsub,corr["corrNpxlx"],corr["corrNpxly"],sf,corr["corrSubapLoc"])
#    def makeSlopes(img,ncam,nsub,npxlx,npxly,sf,sl):
#        """Need to subtract 0.5 from the results if a correlation image."""
    slopes-=0.5#correlation is pixel centred, not 2x2 centred.
    slopes[:288]=0#not using NGS
    if retcorr:
        return slopes,usenow,corr
    else:
        return slopes,usenow

if __name__ == '__main__':
    nfr = 100
    pad = 8
    d=darc.Control("SH")
    img=d.SumData("rtcCalPxlBuf",nfr)[0]/nfr
    #print img.size - 1920*1080
    #data = img.reshape(1080,1920)
    #plt.imshow(data)
    #plt.gca().invert_yaxis()
    #plt.show()
    nacts = 140 #The total number of actuators for the system.
    ncam = 1    #This is the number of camera objects in the system
    npxly = numpy.zeros((ncam,), numpy.int32)#An array of length ncam, specifying the number of pixels in a vertical direction with an entry for each frame grabber.
    npxly[:] = 1080#An array of length ncam, specifying the number of pixels in a vertical direction with an entry for each frame grabber.
    npxlx = npxly.copy()#An array of length ncam, specifying the number of pixels in a horizontal direction with an entry for each frame grabber.
    npxlx[:] = 1920#An array of length ncam, specifying the number of pixels in a horizontal direction with an entry for each frame grabber.
    nsuby = npxly.copy()
    nsuby[:] = 1#this is science, so only one subap required... 
    nsubx = nsuby.copy()
    nsub = nsubx*nsuby #An array with ncam entries, specifying the number of sub-apertures for each frame grabber.
    nsubaps = (nsuby*nsubx).sum() #nsubaps is the total number of sub-apertures
    subapFlag = numpy.ones((nsubaps,), "i") #An array of size equal to the total number of sub-apertures, with a flag value for each, specifying whether this sub-aperture should be used.
    
#    correlation.transformPSF(img,ncam,npxlx,npxly,nsub, subapLocation,d.Get("subapFlag"),pad)
    correlation.transformPSF(img,ncam,npxlx,npxly,nsub, d.Get("subapLocation"),d.Get("subapFlag"),pad,savespace=1)
    #def transformPSF(psf,ncam,npxlx,npxly,nsub,subapLocation,subflag,pad=None,savespace=0):
    #    """Function to transform psf into a form that will be usable by the RTC.
    #    psf is eg the LGS spot elongation pattern.  ncam is number of cameras
    #    npxlx/y is array of size ncam with number of pixels for each camera nsubx/y
    #    is array size ncam with number of subaps for each camera subapLocation is
    #    array containing subap location details, one set of entries per
    #    subaperture.  If pad is set, it will pad the fft pattern, and also return
    #    lots of other things required by darc.  If savespace is also set (as per
    #    default), the returned fft pattern subaperture locations will bear no
    #    resemblance to the wavefront sensors.
    (slopes, usenow) = getSlopes(img)
    print slopes
    print usenow
    print slopes.size
