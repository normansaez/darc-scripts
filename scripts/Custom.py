'''
Gross SH Subap layout
'''
import FITS
import numpy as np
from skimage.morphology import label
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import pylab

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
for i in props:
    x0 = i['Centroid'][0]
    y0 = i['Centroid'][1]
    
    px = x0 + side
    py = y0 + side
    
    px = x0 + side
    my = y0 - side

    mx = x0 - side
    py = y0 + side

    mx = x0 - side
    my = y0 - side

    plt.plot(y0,x0,'xr',markersize=8)

    plt.plot(py,px,'.y',markersize=2)
    plt.plot(py,mx,'.y',markersize=2)
    plt.plot(my,px,'.y',markersize=2)
    plt.plot(my,mx,'.y',markersize=2)
plt.imshow(raw_data, cmap=pylab.gray())
plt.gca().invert_yaxis()
plt.show()
print len(props)
