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


tr = 0.42
side = 8 #pixels
print tr
print 
data = FITS.Read('myfits.fits')
headers = data[0]
raw_data = data[1]
###############################################
print "Print FIT data"
print headers["parsed"]
#npxlx =np.array(eval(data[0]["parsed"]["npxlx"]))
#npxly =np.array(eval(data[0]["parsed"]["npxly"]))
#nsub  =np.array(eval(data[0]["parsed"]["nsub"]))
#print npxlx
#print npxly
#print nsub
##############################################
raw_data = im2bw(raw_data, tr)
label_img = label(raw_data)
props = regionprops(label_img, ['Centroid'])
plt.figure(num=1, figsize=(8, 6), dpi=150, facecolor='w', edgecolor='k')
new_subap = np.array([], dtype = int)
for i in props:
    x0 = i['Centroid'][0]
    y0 = i['Centroid'][1]
    
    x_end = x0 + side
    y_end = y0 + side
    
    #x_end = x0 + side
    #y_start = y0 - side

    #x_start = x0 - side
    #y_end = y0 + side

    x_start = x0 - side
    y_start = y0 - side

    new_subap = np.append(new_subap,[[int(math.floor(y_start)),int(math.floor(y_end)),1,int(math.floor(x_start)),int(math.floor(x_end)),1]])
    #plt.plot(y0,x0,'xr',markersize=8)

    #plt.plot(y_end,x_end,'.y',markersize=2)
    #plt.plot(y_end,x_start,'.y',markersize=2)
    #plt.plot(y_start,x_end,'.y',markersize=2)
    #plt.plot(y_start,x_start,'.y',markersize=2)
#plt.imshow(raw_data, cmap=pylab.gray())
#plt.gca().invert_yaxis()
#plt.show()
nsub = len(props)
npxlx = 640
npxly = 480

new_subap = new_subap.reshape(new_subap.size/6,6)

print new_subap
subflag = np.ones((nsub,),dtype=int)
fname="newSubAp.fits"
#{'END': '', 'npxly': '[480]', 'EXTEND': 'T', 'SIMPLE': 'T', 'NAXIS2': '182', 'NAXIS': '2', 'NAXIS1': '6', 'BITPIX': '32', 'npxlx': '[640]', 'nsub': '[182]'}
FITS.Write(new_subap,fname,extraHeader=["npxlx   = '[%s]'"%str(npxlx),"npxly   = '[%s]'"%str(npxly),"nsub    = '[%s]'"%str(nsub)])
FITS.Write(subflag,fname,writeMode='a')
#print new_ap.shape
#print new_ap.size

