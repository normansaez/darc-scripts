#!/usr/bin/python

'''
Gross SH Subap layout
'''
import FITS
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage.morphology import label
from skimage.measure import regionprops

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
    '''
    Get the image from set in darc
    '''
    #import darc
    #c=darc.Control("main")
    #bg = c.Get("bgImage")
    #data = bg.reshape(480, 640)
    #FITS.Write(data, 'myfits.fits', writeMode='a')
    #headers = data[0]
    #raw_data = data[1]
    #return headers, raw_data
    return

def get_image():
    '''
    Get image from fit file
    '''
    data = FITS.Read('myfits.fits')
    headers = data[0]
    raw_data = data[1]
    return headers, raw_data

def get_props(raw_data, threshold):
    '''
    Using raw data from fits, get properties such as Centroid
    '''
    raw_data = im2bw(raw_data, threshold)
    label_img = label(raw_data)
    props = regionprops(label_img, ['Centroid'])
    return props

def get_centroids(props):
    '''
    Using properties as centroid(x, y) , get them as two vectors: x and y
    '''
    centroid_x = np.array([], "i")
    centroid_y = np.array([], "i")
    for i in props:
        x0 = i['Centroid'][0]
        y0 = i['Centroid'][1]
        centroid_x = np.append(centroid_x, [[int(math.floor(x0))]])
        centroid_y = np.append(centroid_y, [[int(math.floor(y0))]])
    return centroid_x, centroid_y

def is_centroid_in_subap(c_x, c_y, startx, starty, width, height):
    '''
    Check if the centroid is inside a subap or not
    '''
    x_in = 0
    y_in = 0
    if abs(startx - c_x) < width:
        x_in = 1
    if abs(starty - c_y) < height:
        y_in = 1
    return x_in * y_in


############## START HERE ############################
threshold = 0.42 #threshold
nsubx = 15
nsuby = 15
xspace = 0.01
yspace = 0.01
color = {0:'black', 1:'green', 2:'red', 3:'blue', 4:'gray', 5:'purple'}

nsubs = nsubx*nsuby
subapLocation = np.array([], "i")
subapFlag = np.array([], "i")

print "Threshole: %.3f\nnsubx * nsuby = nsubs <-> %dx%d=%d"  % (threshold, nsubx, nsuby, nsubs)

###############################################
#Get centroid of each point.
headers, raw_data = get_image()
props = get_props(raw_data, threshold)
centroid_x, centroid_y = get_centroids(props)

#make mask
x_max = centroid_x.max()  
y_max = centroid_y.max() 
x_min = centroid_x.min() 
y_min = centroid_y.min() 

npxlx =  math.floor(x_max-x_min)
npxly =  math.floor(y_max-y_min)
npxlx_pf = npxlx/nsubx
npxly_pf = npxly/nsuby
print "pxl x:%d" % npxlx
print "pxl y:%d" % npxly
print "pxl x:%.3f p/f" % npxlx_pf 
print "pxl y:%.3f p/f" % npxly_pf


for i in range(nsubx):
    for j in range(nsuby):
        c = divmod(j, 5)[1]
        width, height = npxlx_pf/x_max, npxly_pf/y_max
        xy = (x_min/x_max)+i*(npxlx_pf/x_max + xspace), y_min/y_max + j*(npxly_pf/y_max + yspace),
        p = mpatches.Rectangle(xy, width, height, facecolor=color[c], edgecolor=color[c])
        plt.gca().add_patch(p)
        for ii in range(len(centroid_x)):
            is_valid = is_centroid_in_subap(centroid_x[ii], centroid_y[ii], (x_min)+i*(npxlx_pf + xspace), y_min + j*(npxly_pf + yspace), width*x_max, height*y_max)
            if is_valid:
                break
            else:
                pass
                
        subapFlag = np.append(subapFlag, [[is_valid]])
plt.draw()
#plt.gca().invert_yaxis()
plt.show()

print subapFlag.reshape(15, 15)
#fname="newSubApLocation.fits"
#FITS.Write(valid_subapLocation, fname, extraHeader=["npxlx   = '[%s]'"%str(npxlx), "npxly   = '[%s]'"%str(npxly), "nsubaps    = '[%s]'"%str(nsubaps)])
#FITS.Write(subFlag, fname, writeMode='a')
