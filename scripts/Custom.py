'''
Gross SH Subap layout
'''
import FITS
import numpy as np
from skimage.morphology import label
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import pylab
import math
from pylab import *

class MouseMonitor:
    event = None
    xdatalist = []
    ydatalist = []

    def mycall(self, event):
        self.event = event
        self.xdatalist.append(event.xdata)
        self.ydatalist.append(event.ydata)
        
        print 'x = %s and y = %s' % (event.xdata,event.ydata)
        
        ax = gca()  # get current axis
        ax.hold(True) # overlay plots.
        
        # Plot a red circle where you clicked.
        ax.plot([event.xdata],[event.ydata],'ro')
        
        draw()  # to refresh the plot.
        return [event.xdata,event.ydata]

def im2bw(image, threshold):
    '''
    Convert a numpy.array float image to binary image, given a threshold
    '''
    (axis_x, axis_y) = image.shape
    image = image/image.max()
    img = np.zeros((axis_x, axis_y))
    for i in range(0, axis_x):
        for j in range(0, axis_y):
            if image[i][j] >= threshold:
                img[i][j] = 1
            else:
                img[i][j] = 0
    return img

############## START HERE ############################
tr = 0.42 #threshold
side = 8 #pixels
print tr

############## DARC #######################
import darc
c=darc.Control("main")
bg = c.Get("bgImage")
data = bg.reshape(480,640)
FITS.Write(data,'myfits.fits',writeMode='a')
data = FITS.Read('myfits.fits')
############## DARC #######################

headers = data[0]
raw_data = data[1]
###############################################
raw_data = im2bw(raw_data, tr)
label_img = label(raw_data)
props = regionprops(label_img, ['Centroid'])
plt.figure(num=1, figsize=(8, 6), dpi=150, facecolor='w', edgecolor='k')
new_subapLocation = np.array([], "i")
new_subapFlag = np.array([], "i")
new_centroid = np.array([], "i")

for i in props:
    x0 = i['Centroid'][0]
    y0 = i['Centroid'][1]
    new_centroid = np.append(new_centroid,[[int(math.floor(x0)),int(math.floor(y0))]])
    
    x_end = x0 + side
    y_end = y0 + side
    
    x_start = x0 - side
    y_start = y0 - side

    new_subapLocation = np.append(new_subapLocation,[[int(math.floor(y_start)),int(math.floor(y_end)),1,int(math.floor(x_start)),int(math.floor(x_end)),1]])
    plt.plot(y0,x0,'xr',markersize=8)

    plt.plot(y_end,x_end,'.y',markersize=2)
    plt.plot(y_end,x_start,'.y',markersize=2)
    plt.plot(y_start,x_end,'.y',markersize=2)
    plt.plot(y_start,x_start,'.y',markersize=2)
plt.imshow(raw_data, cmap=pylab.gray())
plt.gca().invert_yaxis()

#get first point in subap centroid maps.
mouse = MouseMonitor()
connect('button_press_event', mouse.mycall)
plt.show()

print int(mouse.event.xdata)
print int(mouse.event.ydata)
#TODO this should be get from some other place !
nsub = len(props)
npxlx = 640
npxly = 480

new_subapLocation = new_subapLocation.reshape(new_subapLocation.size/6,6)

print new_subapLocation
print nsub
subflag = np.ones((nsub,),dtype=int)
fname="newSubApLocation.fits"
#{'END': '', 'npxly': '[480]', 'EXTEND': 'T', 'SIMPLE': 'T', 'NAXIS2': '182', 'NAXIS': '2', 'NAXIS1': '6', 'BITPIX': '32', 'npxlx': '[640]', 'nsub': '[182]'}
FITS.Write(new_subapLocation,fname,extraHeader=["npxlx   = '[%s]'"%str(npxlx),"npxly   = '[%s]'"%str(npxly),"nsub    = '[%s]'"%str(nsub)])
FITS.Write(subflag,fname,writeMode='a')
#print new_ap.shape
FITS.Write(new_centroid,'r_centroid.fits',extraHeader=["npxlx   = '[%s]'"%str(npxlx),"npxly   = '[%s]'"%str(npxly),"nsub    = '[%s]'"%str(nsub)])
#print new_ap.size

