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

def get_subflag(nsubx, nsuby, x0, y0, centroids):
    nsub = nsubx * nsuby
    subFlag = np.ones((nsub,),"i")
    subFlag = subFlag.reshape(nsubx,nsuby)
    #########Q1##########
    subFlag[0,0] = 0  
    subFlag[0,1] = 0  
    subFlag[0,2] = 0  
    subFlag[0,3] = 0  
    subFlag[0,4] = 0
    #------------------
    subFlag[0,11] = 0  
    subFlag[0,12] = 0  
    subFlag[0,13] = 0  
    subFlag[0,14] = 0  

    ######################
    subFlag[1,0] = 0  
    subFlag[1,1] = 0  
    #------------------
    subFlag[1,12] = 0  
    subFlag[1,13] = 0  
    subFlag[1,14] = 0  
    ######################
    subFlag[2,0] = 0  
    #------------------
    subFlag[2,13] = 0  
    subFlag[2,14] = 0  
    ######################
    subFlag[3,0] = 0  
    #
    subFlag[:,14] = 0

##########################################
    subFlag[14,0] = 0  
    subFlag[14,1] = 0  
    subFlag[14,2] = 0  
    subFlag[14,3] = 0  
    #-------14----------
    subFlag[14,10] = 0  
    subFlag[14,11] = 0  
    subFlag[14,12] = 0  
    subFlag[14,13] = 0  
    subFlag[14,14] = 0 
    #
    subFlag[13,0] = 0  
    subFlag[13,1] = 0  
    subFlag[13,2] = 0  
    #-------13----------
    subFlag[13,12] = 0  
    subFlag[13,13] = 0  
    subFlag[13,14] = 0  
    #
    subFlag[12,0] = 0  
    subFlag[12,1] = 0  
    #-------12----------
    subFlag[12,13] = 0  
    subFlag[12,14] = 0  
    #
    subFlag[11,0] = 0  
    #-------11----------
    subFlag[11,14] = 0  

    return subFlag
def _get_subflag(nsubx, nsuby, x0, y0, centroids):
    '''
    '''
    print "get_subflag debug"
    pxl_to_search = 40
    nsub = nsubx * nsuby
    subFlag = np.zeros((nsub,),"i")
    for i in range(0,len(centroids),2):
        x = centroids[i]
        y = centroids[i+1]
        x0 = x0 + pxl_to_search
        for count in range(nsub):
            print "looking %d - %d = %d? %d"%(x0,x,abs(x0-x),2*pxl_to_search)
            if abs(x0 - x) <= pxl_to_search*2:
                print "--->in<---"
                subFlag[count] = 1
                break
            else:
                print "--->out<---"
        x0 = x0 + pxl_to_search
#        raw_input("")            
    return subFlag

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
#import darc
#c=darc.Control("main")
#bg = c.Get("bgImage")
#data = bg.reshape(480,640)
#FITS.Write(data,'myfits.fits',writeMode='a')
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
#mouse = MouseMonitor()
#connect('button_press_event', mouse.mycall)
plt.show()

#x0 = int(mouse.event.xdata)
#y0 = int(mouse.event.ydata)

#TODO this should be get from some other place !
npxlx = 640
npxly = 480

nsubx = 15
nsuby = 15

nsub = nsubx * nsuby

#Writing fit for fot coordinate:
fname="newSubApLocation.fits"
subFlag = get_subflag(nsubx, nsuby, x0, y0, new_centroid)
print subFlag.reshape(nsubx,nsuby)

new_subapLocation = new_subapLocation.reshape(new_subapLocation.size/6,6)
FITS.Write(new_subapLocation,fname,extraHeader=["npxlx   = '[%s]'"%str(npxlx),"npxly   = '[%s]'"%str(npxly),"nsub    = '[%s]'"%str(nsub)])
FITS.Write(subFlag,fname,writeMode='a')

# Only centroid coordinates
FITS.Write(new_centroid,'centroid_coordinatesXY.fits',extraHeader=["npxlx   = '[%s]'"%str(npxlx),"npxly   = '[%s]'"%str(npxly),"nsub    = '[%s]'"%str(nsub)])
