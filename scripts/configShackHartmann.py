#darc, the Durham Adaptive optics Real-time Controller.
#Copyright (C) 2010 Alastair Basden.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#A configuration file for use with the uEye USB camera.
'''
Use with --prefix=ShackHartmann
'''
#import FITS
#import tel
import numpy

nacts = 140 #The total number of actuators for the system.
ncam = 1    #This is the number of camera objects in the system
ncamThreads = numpy.ones((ncam,), numpy.int32)*1#An array of length ncam, with a value for each frame grabber specifying the number of threads for each
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

#subapFlag = tel.Pupil(11,11/2.,1,11).subflag.astype("i").ravel()#numpy.ones((nsubaps,),"i")

ncents = subapFlag.sum()*2 #Number of centroids, each centroid 2 elements = (x,y). That's because subapFlag*2
npxls = (npxly*npxlx).sum()#Number of pixels

fakeCCDImage = None#(numpy.random.random((npxls,))*20).astype("i")
#camimg = (numpy.random.random((10,npxls))*20).astype(numpy.int16)

bgImage = None#FITS.Read("shimgb1stripped_bg.fits")[1].astype("f")#numpy.zeros((npxls,),"f")
darkNoise = None#FITS.Read("shimgb1stripped_dm.fits")[1].astype("f")
flatField = None#FITS.Read("shimgb1stripped_ff.fits")[1].astype("f")
#indx = 0
#nx = npxlx/nsubx
#ny = npxly/nsuby
#correlationPSF = numpy.zeros((npxls,),numpy.float32)

subapLocation = numpy.zeros((nsubaps, 6), "i")#For each sub-aperture there are then 6 values, [ystart, yend, ystep, xstart, xend, xstep]. These are the pixel values that the sub-aperture starts and finishes at, and the number of rows or columns to step.
nsubaps = nsuby*nsubx#cumulative subap, nsubaps is the total number of sub-apertures
nsubapsCum = numpy.zeros((ncam+1,), numpy.int32)
ncentsCum = numpy.zeros((ncam+1,), numpy.int32)
for i in range(ncam):
    nsubapsCum[i+1] = nsubapsCum[i]+nsubaps[i]
    ncentsCum[i+1] = ncentsCum[i]+subapFlag[nsubapsCum[i]:nsubapsCum[i+1]].sum()*2
xoff = 0
yoff = 0
nx = (npxlx[0]-2*xoff)/nsubx[0]
ny = (npxly[0]-2*yoff)/nsuby[0]
for i in range(nsubaps):
    subapLocation[i] = ((i//nsubx[0])*ny+yoff, (i//nsubx[0]+1)*ny+yoff, 1, (i%nsubx[0])*nx+xoff, (i%nsubx[0]+1)*nx+xoff, 1)

#setting prefix
try:
    a = prefix
except:
    prefix = "main"

#guid for red camera gruppy is 2892819690320999
#guid for fire-i camera is 582164335728668360
#guid for red camera pike is 2892819656758559
if prefix == "main":
    #to select fire-i camera (unibrain fire-i)
    guid = 582164335728668360
    vmode = 69
    fr = 36 #30Hz
    color = -1 #357
    width = 640
    height = 480
elif prefix == "sci":
    #to select red camera (gruppy)
    guid = 2892819690320999
    vmode = 70
    fr = 35#15Hz
    color = -1 #357
    width = 640
    height = 480
else:
    guid = 2892819656758559#to select pike (new camera)
    vmode = 88#for the red camera
    fr = 35#15Hz
    color = -1 #357
    width = 1920
    height = 1080
cameraParams = numpy.array([guid, guid, 1, vmode, color, width, height, 0, 0, fr, 2]).astype(numpy.int32)
#cameraParams: An array of 32 bit integers which is passed into the camera object to configure it.
#[0] guid,
#[1] guid,
#[2] print,
#[3] vidmode(-1 or 69(8bit)/70(16bit) probably),
#[4] color mode when vidmode==-1 (8=352, 16=357 or -1), 
#[5] width(640), 
#[6] height(480), 
#[7] offx (0), o
#[8] ffy (0), 
#[9] framerate (36==30Hz, 35, -1==15Hz), 
#[10] [ISO speed (-1==don't set, 0=100, 1=200,2=400 (probably want -1 or 2), 3=800,4=1600,5=3200.)]

#Overwrite guid, because they are uint64
lval = cameraParams[:2].view(numpy.uint64)
lval[0] = guid

rmx = numpy.zeros((nacts, ncents), "f")#The reconstructor matrix, shape nacts, ncents. Used only when the matrix- vector reconstruction interface is used.

mirrorParams = numpy.zeros((3,), "i")#The parameters supplied to the mirror library, an array of 32 bit integers, con- tents depending on the mirror library
mirrorParams[0] = 1
mirrorParams[1] = 1
mirrorParams[2] = -1
pxlCnt = numpy.zeros((nsubaps,), numpy.int32) #An array of size equal to the total number of sub-apertures. The entries are the total number of pixels that are required for each sub-aperture before processing of this sub-aperture can commence. Note this can be computed from subapLo- cation though is given as a parameter to allow extra flexibility. To allow the RTC to process multiple sub-apertures before commencing reconstruction, these sub-apertures should have the same pxlCnt value.

for k in range(ncam):
    # tot=0#reset for each camera
    for i in range(nsub[k]):
        #for j in range(nsubx[k]):
        indx = nsubapsCum[k]+i#*nsubx[k]+j
        n = (subapLocation[indx, 1]-1)*npxlx[k]+subapLocation[indx, 4]
        pxlCnt[indx] = n

control = {
    "switchRequested":0,#this is the only item in a currently active buffer that can be changed...
    "pause":0,#A flag, which if set pauses the RTC (though camera frames are still read). No image calibration, slope calculation or DM vector computation is carried out.
    "go":1,#When set to zero, the RTC will stop and exit.
    #"DMgain":0.25,
    #"staticTerm":None,
    "maxClipped":nacts,#The maximum number of actuators allowed to be clipped before an error is raised.
    "refCentroids":None,#An array of size equal to twice the total number of valid sub-apertures. Specify the reference slope measurements (or None) which are subtracted from slope measurements.
    "centroidMode":"CoG",#whether data is from cameras or from WPU.
    "windowMode":"basic",#“basic”, “adaptive” or “global”
    "thresholdAlgo":0,#The thresholding algorithm to be used. If equal to 1, values less than the threshold are set to zero. If equal to 2, the threshold is subtracted from all values, and negative values are set to zero. Other values mean no thresholding. Used only by the calibration interface module.
    #"acquireMode":"frame",#frame, pixel or subaps, depending on what we should wait for...
    "reconstructMode":"simple",#simple (matrix vector only), truth or open.A string with value equal to one of “simple”, “truth”, “open” or “offset”.
    "centroidWeight":None,
    "v0":numpy.zeros((nacts,), "f"),#v0 from the tomograhpcic algorithm in openloop (see spec).Initial voltages (actually DAC values) used, one per actuator.
    #"gainE":None,#numpy.random.random((nacts,nacts)).astype("f"),#E from the tomo algo in openloop (see spec) with each row i multiplied by 1-gain[i]
    #"clip":1,#use actMax instead
    "bleedGain":0.0,#0.05,#a gain for the piston bleed...
    #"midRangeValue":2048,#midrange actuator value used in actuator bleed
    "actMax":numpy.ones((nacts,), numpy.uint16)*65535,#4095,#max actuator value .The maximum allowed actuator value, per actuator.
    "actMin":numpy.zeros((nacts,), numpy.uint16),#4095,#max actuator value. The minimum allowed actuator value, per actuator.
    #"gain":numpy.zeros((nacts,),numpy.float32),#the actual gains for each actuator...
    "nacts":nacts,
    "ncam":ncam,
    "nsub":nsuby*nsubx,
    #"nsubx":nsubx,
    "npxly":npxly,
    "npxlx":npxlx,
    "ncamThreads":ncamThreads,
    "pxlCnt":pxlCnt,
    "subapLocation":subapLocation,
    "bgImage":bgImage,
    "darkNoise":darkNoise,
    "closeLoop":1,
    "flatField":flatField,#numpy.random.random((npxls,)).astype("f"),
    "thresholdValue":0.,
    "powerFactor":1.,#raise pixel values to this power.
    "subapFlag":subapFlag,
    "fakeCCDImage":fakeCCDImage,
    "printTime":0,#whether to print time/Hz
    "rmx":rmx,#numpy.random.random((nacts,ncents)).astype("f"),
    "gain":numpy.ones((nacts,), "f"),#The actuator gain, and array of size nacts, specifying the unique gain for each actuator.
    "E":numpy.zeros((nacts,nacts), "f"),#E from the tomoalgo in openloop.
    "threadAffinity":None,
    "threadPriority":numpy.ones((ncamThreads.sum()+1,), numpy.int32)*10,
    "delay":0,
    "clearErrors":0,
    "camerasOpen":1, #A flag used to open the camera shared object library
    "cameraName":"libcamfirewire.so",#"libsl240Int32cam.so",#"camfile",
    "cameraParams":cameraParams,
    "mirrorName":"libmirrorBMMMulti.so",
    "mirrorParams":mirrorParams,
    "mirrorOpen":0,
    "frameno":0,
    "switchTime":numpy.zeros((1,), "d")[0],
    "adaptiveWinGain":0.5,
    "nsubapsTogether":1,
    "nsteps":0,
    "addActuators":0,
    "actuators":numpy.ones((nacts,), numpy.float32)*32768,#None,#(numpy.random.random((3,52))*1000).astype("H"),#None,#an array of actuator values.
    "actSequence":None,#numpy.ones((3,),"i")*1000,
    "recordCents":0,
    "pxlWeight":None,
    "averageImg":0,
    "actuatorMask":None,
    "averageCent":0,
    "centCalData":None,
    "centCalBounds":None,
    "centCalSteps":None,
    "figureOpen":0,
    "figureName":"libfigureSL240.so",
    "figureParams":None,
    "reconName":"libreconmvm.so",
    "fluxThreshold":0,
    "printUnused":1,
    "useBrightest":0,
    "figureGain":1,
    "decayFactor":None,#used in libreconmvm.so
    "slopeOpen":0,
    "reconlibOpen":0,
    "maxAdapOffset":0,
#    "mirrorStep":0,
#    "mirrorSteps":numpy.zeros((nacts,),numpy.int32),
#    "mirrorUpdate":0,
#    "mirrorReset":0,
#    "mirrorGetPos":0,
#    "mirrorDoMidRange":0,
#    "mirrorMidRange":numpy.ones((nacts,),numpy.int32)*500,
    "actInit":None,
    "actMapping":None,
    "actOffset":None,
    "actScale":None,
    "actSource":None,
    }
