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

############## START HERE ############################
tr = 0.42 #threshold
side = 8 #pixels
nsubx = 15
nsuby = 15
nsubs = nsubx*nsuby

print "Threshole: %.3f\nSide: %d\nnsubx * nsuby = nsubs <-> %dx%d=%d"  % (tr,side,nsubx,nsuby,nsubs)

############## DARC #######################
#import darc
#c=darc.Control("main")
#bg = c.Get("bgImage")
#data = bg.reshape(480,640)
#FITS.Write(data,'myfits.fits',writeMode='a')
data = FITS.Read('myfits.fits')
############## DARC #######################
# get headers and raw_data 
headers = data[0]
raw_data = data[1]
###############################################
#Get centroid of each point.
raw_data = im2bw(raw_data, tr)
label_img = label(raw_data)
props = regionprops(label_img, ['Centroid'])
############### ############## ####################
plt.figure(num=1, figsize=(8, 6), dpi=150, facecolor='w', edgecolor='k')

# Init variables
valid_subapLocation = np.array([], "i")
new_subapFlag = np.array([], "i")
centroid_x = np.array([], "i")
centroid_y = np.array([], "i")

# Fill new centroid.
for i in props:
    x0 = i['Centroid'][0]
    y0 = i['Centroid'][1]
    centroid_x = np.append(centroid_x,[[int(math.floor(x0))]])
    centroid_y = np.append(centroid_y,[[int(math.floor(y0))]])

x0 = centroid_x.max() + side/2.0  
y0 = centroid_y.max() + side/2.0

x1 = centroid_x.min() + side/2.0
y1 = centroid_y.min() + side/2.0

x2 = centroid_x.max() + side/2.0
y2 = centroid_y.min() + side/2.0

x3 = centroid_x.min() + side/2.0
y3 = centroid_y.max() + side/2.0

#plt.plot(y0,x0,'ok',markersize=12) #this one
#plt.plot(y1,x1,'og',markersize=12) #this one
#plt.plot(y2,x2,'or',markersize=12)
#plt.plot(y3,x3,'ob',markersize=12)
#plt.gca().invert_yaxis()
#plt.show()

cxmax = centroid_x.max() + 100
cymax = centroid_y.max() + 100

print "pxl en total x: %d" % ((centroid_x.max() - centroid_x.min()))
print "pxl en total y: %d" % ((centroid_y.max() - centroid_y.min()))
npxlx =  math.floor((centroid_x.max() - centroid_x.min())/nsubx)
npxly =  math.floor((centroid_y.max() - centroid_y.min())/nsuby)
print "pxl x:%d" % npxlx
print "pxl y:%d" % npxly

x0 = x0/cxmax
y0 = y0/cymax

x1 = x1/cxmax
y1 = y1/cymax

x2 = x2/cxmax
y2 = y2/cymax

x3 = x3/cxmax
y3 = y3/cymax


print x0
print y0
print "---" 
print x1
print y1
print "---"
print x2
print y2
print "---"
print x3
print y3


width, height = 0.05, 0.05

xy = y0, x0,
p = mpatches.Rectangle(xy, width, height, facecolor="black", edgecolor="black")
plt.gca().add_patch(p)
xy = y1, x1,
p = mpatches.Rectangle(xy, width, height, facecolor="green", edgecolor="green")
plt.gca().add_patch(p)
xy = y2, x2,
p = mpatches.Rectangle(xy, width, height, facecolor="red", edgecolor="red")
plt.gca().add_patch(p)
xy = y3, x3,
p = mpatches.Rectangle(xy, width, height, facecolor="blue", edgecolor="blue")
plt.gca().add_patch(p)


xd = (x0 - x1)/(nsubx)
yd = (y0 - y1)/(nsuby)
print "----------------------------------"
print xd
print yd
print "----------------------------------"
yspace = 0.01
xspace = 0.01
color = {0:'black',1:'green',2:'red',3:'blue',4:'gray'}

for sidex in range(nsubx):
    for sidey in range(nsuby):
#        print "(%2d,%2d)" %(sidex,sidey),
        print "(%.3f,%.3f)" %(y1,x1),
        xy = y1, x1,
        try:
            p = mpatches.Rectangle(xy, width, height, facecolor=color[sidey], edgecolor=color[sidey])
        except:
            p = mpatches.Rectangle(xy, width, height, facecolor='purple', edgecolor='purple') 
        plt.gca().add_patch(p)
        y1 = y1 + yd
#        x1 = x1 + xd
    print
    x1 = x1 + xd
plt.draw()
plt.gca().invert_yaxis()
plt.show()


#    valid_subapLocation = np.append(valid_subapLocation,[[int(math.floor(y_start)),int(math.floor(y_end)),1,int(math.floor(x_start)),int(math.floor(x_end)),1]])
##get first point in subap centroid maps.
#mouse = MouseMonitor()
#connect('button_press_event', mouse.mycall)
#plt.show()
#
#x0 = int(mouse.event.xdata)
#y0 = int(mouse.event.ydata)

#fname="newSubApLocation.fits"
#subFlag = get_subflag(nsubx, nsuby, x_init, y_init, centroid_x)
#FITS.Write(valid_subapLocation,fname,extraHeader=["npxlx   = '[%s]'"%str(npxlx),"npxly   = '[%s]'"%str(npxly),"nsubaps    = '[%s]'"%str(nsubaps)])
#FITS.Write(subFlag,fname,writeMode='a')

# Only centroid coordinates
#FITS.Write(centroid_x,'centroid_coordinatesXY.fits',extraHeader=["npxlx   = '[%s]'"%str(npxlx),"npxly   = '[%s]'"%str(npxly),"nsubaps    = '[%s]'"%str(nsubaps)])
