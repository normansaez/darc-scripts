'''
Gross SH Subap layout
'''
import FITS
import numpy as np
from skimage.morphology import label
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
        ax.plot([event.xdata],[event.ydata],'go',markersize=2)
        
        draw()  # to refresh the plot.
        return [event.xdata,event.ydata]

def get_subflag(nsubx, nsuby, x0, y0, centroids):
    nsubaps = nsubx * nsuby
    subFlag = np.ones((nsubaps,),"i")
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
    nsubaps = nsubx * nsuby
    subFlag = np.zeros((nsubaps,),"i")
    for i in range(0,len(centroids),2):
        x = centroids[i]
        y = centroids[i+1]
        x0 = x0 + pxl_to_search
        for count in range(nsubaps):
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

def get_image_from_darc():
    ############## DARC #######################
    import darc
    c=darc.Control("main")
    bg = c.Get("bgImage")
    data = bg.reshape(480,640)
    #FITS.Write(data,'myfits.fits',writeMode='a')
    headers = data[0]
    raw_data = data[1]
    return headers, raw_data
    
def get_image():
    data = FITS.Read('myfits.fits')
    headers = data[0]
    raw_data = data[1]
    return headers, raw_data

def get_props(raw_data,tr):
    raw_data = im2bw(raw_data, tr)
    label_img = label(raw_data)
    props = regionprops(label_img, ['Centroid'])
    return props


def get_centroids(props):
    centroid_x = np.array([], "i")
    centroid_y = np.array([], "i")
    for i in props:
        x0 = i['Centroid'][0]
        y0 = i['Centroid'][1]
        centroid_x = np.append(centroid_x,[[int(math.floor(x0))]])
        centroid_y = np.append(centroid_y,[[int(math.floor(y0))]])
    return centroid_x, centroid_y

def check_in_subapp(cx,cy,startx,starty,width,height):
    x_in = 0
    y_in = 0
    if abs(startx - cx) < width:
        x_in = 1
    if abs(starty - cy) < height:
        y_in = 1
    return x_in * y_in

############## START HERE ############################
tr = 0.42 #threshold
nsubx = 15
nsuby = 15
nsubs = nsubx*nsuby

subapLocation = np.array([], "i")
subapFlag = np.array([], "i")
print "Threshole: %.3f\nnsubx * nsuby = nsubs <-> %dx%d=%d"  % (tr,nsubx,nsuby,nsubs)

###############################################
#Get centroid of each point.
headers, raw_data = get_image()
props = get_props(raw_data,tr)
centroid_x, centroid_y = get_centroids(props)

#make mask
x_max = centroid_x.max()  
y_max = centroid_y.max() 
x_min = centroid_x.min() 
y_min = centroid_y.min() 

xspace = 0.01
yspace = 0.01
npxlx =  math.floor(x_max-x_min)
npxly =  math.floor(y_max-y_min)
npxlx_pf = npxlx/nsubx
npxly_pf = npxly/nsuby
print "pxl x:%d" % npxlx
print "pxl y:%d" % npxly
print "pxl x:%.3f p/f" % npxlx_pf 
print "pxl y:%.3f p/f" % npxly_pf


color = {0:'black',1:'green',2:'red',3:'blue',4:'gray',5:'purple'}
for i in range(nsubx):
    for j in range(nsuby):
        c = divmod(j,5)[1]
        width, height = npxlx_pf/x_max, npxly_pf/y_max
        xy = (x_min/x_max)+i*(npxlx_pf/x_max + xspace), y_min/y_max + j*(npxly_pf/y_max + yspace),
        p = mpatches.Rectangle(xy, width, height, facecolor=color[c], edgecolor=color[c])
        plt.gca().add_patch(p)
        for ii in range(len(centroid_x)):
            valid = check_in_subapp(centroid_x[ii],centroid_y[ii], (x_min)+i*(npxlx_pf + xspace), y_min + j*(npxly_pf + yspace),width*x_max, height*y_max)
            if valid:
                break
            else:
                pass
                
        subapFlag = np.append(subapFlag,[[valid]])
plt.draw()
#plt.gca().invert_yaxis()
plt.show()

print subapFlag.reshape(15,15)
##Image properties
#plt.figure(num=1, figsize=(8, 6), dpi=150, facecolor='w', edgecolor='k')
##    valid_subapLocation = np.append(valid_subapLocation,[[int(math.floor(y_start)),int(math.floor(y_end)),1,int(math.floor(x_start)),int(math.floor(x_end)),1]])
###get first point in subap centroid maps.
##mouse = MouseMonitor()
##connect('button_press_event', mouse.mycall)
##plt.show()
##
##x0 = int(mouse.event.xdata)
##y0 = int(mouse.event.ydata)
#
##fname="newSubApLocation.fits"
##subFlag = get_subflag(nsubx, nsuby, x_init, y_init, centroid_x)
##FITS.Write(valid_subapLocation,fname,extraHeader=["npxlx   = '[%s]'"%str(npxlx),"npxly   = '[%s]'"%str(npxly),"nsubaps    = '[%s]'"%str(nsubaps)])
##FITS.Write(subFlag,fname,writeMode='a')
#
## Only centroid coordinates
##FITS.Write(centroid_x,'centroid_coordinatesXY.fits',extraHeader=["npxlx   = '[%s]'"%str(npxlx),"npxly   = '[%s]'"%str(npxly),"nsubaps    = '[%s]'"%str(nsubaps)])
