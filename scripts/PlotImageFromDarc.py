#import os
#import sys
#import socket
#import time
#import glob
#import numpy
#import gtk
import darc
#import FITS
#import correlation
#import calibrate
#import matplotlib
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#import pylab
#import FITS
import matplotlib.pyplot as plt
#import pylab

d=darc.Control("ShackHartmann")
nfr = 100
img=d.SumData("rtcCalPxlBuf",nfr)[0]/nfr
print img.size - 1920*1080
data = img.reshape(1080,1920)
plt.imshow(data)
plt.gca().invert_yaxis()
plt.show()
