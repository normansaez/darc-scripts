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
threshold = 0.42 
nsubx = 15
nsuby = 15
xspace = 0.01
yspace = 0.01
color_dict = {0:'black', 1:'green', 2:'red', 3:'blue', 4:'gray', 5:'purple',6:'white'}

nsubs = nsubx*nsuby
subapLocation = np.array([], "i")
subFlag = np.array([], "i")

print "Threshole: %.3f\nnsubx * nsuby = nsubs <-> %dx%d=%d"  % (threshold, nsubx, nsuby, nsubs)

###############################################
#Get image and centroid per spot
headers, raw_data = get_image()
props = get_props(raw_data, threshold)
centroid_x, centroid_y = get_centroids(props)

#Calculate subLocation borders
x_max = centroid_x.max()  
y_max = centroid_y.max() 
x_min = centroid_x.min() 
y_min = centroid_y.min() 

npxlx =  math.floor(x_max-x_min) #Total pixels x
npxly =  math.floor(y_max-y_min) #Total pixels y
npxlx_pf = npxlx/nsubx           #x: plx/subap
npxly_pf = npxly/nsuby           #y: plx/subapy
print "pxl x:%d" % npxlx
print "pxl y:%d" % npxly
print "pxl x:%.3f p/f" % npxlx_pf 
print "pxl y:%.3f p/f" % npxly_pf

#This does all the job !
for i in range(nsubx):
    for j in range(nsuby):
        #normalized
        norm_width  = npxlx_pf/x_max
        norm_height = npxly_pf/y_max
        norm_x = x_min/x_max + i*(npxlx_pf/x_max + xspace)
        norm_y = y_min/y_max + j*(npxly_pf/y_max + yspace)
        norm_xy = norm_x, norm_y,
        for index in range(len(centroid_x)):
            #remove normalization
            x_pxl = x_min + i*(npxlx_pf + xspace)
            y_pxl = y_min + j*(npxly_pf + yspace)
            w_pxl = norm_width*x_max
            h_pxl = norm_height*y_max
            is_valid = is_centroid_in_subap(centroid_x[index], centroid_y[index],x_pxl, y_pxl, w_pxl, h_pxl)
            if is_valid:
                break
            else:
                pass
                
        subFlag = np.append(subFlag, [[is_valid]])
        if is_valid:
            p = mpatches.Rectangle(norm_xy, norm_width, norm_height, facecolor=color_dict[1], edgecolor=color_dict[0])
            plt.gca().add_patch(p)
            x_start = centroid_x[index] - npxlx_pf/2.0
            y_start = centroid_y[index] + npxly_pf/2.0
            x_end   = centroid_x[index] + npxlx_pf/2.0
            y_end   = centroid_y[index] - npxly_pf/2.0
            subapLocation = np.append(subapLocation, [[y_start, y_end, 1, x_start, x_end, 1]])
        else:
            p = mpatches.Rectangle(norm_xy, norm_width, norm_height, facecolor=color_dict[6], edgecolor=color_dict[0])
            plt.gca().add_patch(p)
            x_start = x_pxl + h_pxl
            y_start = y_pxl = h_pxl
            x_end   = x_pxl + w_pxl
            y_end   = y_pxl = w_pxl
            subapLocation = np.append(subapLocation, [[y_start, y_end, 1, x_start, x_end, 1]])
            
print subFlag.reshape(15,15)
plt.draw()
plt.gca().invert_yaxis()
plt.show()

fname="newSubApLocation.fits"
FITS.Write(subapLocation, fname, extraHeader=["npxlx   = '[%s]'"%str(nsubx), "npxly   = '[%s]'"%str(nsuby), "nsubaps    = '[%s]'"%str(nsubs)])
FITS.Write(subFlag, fname, writeMode='a')
