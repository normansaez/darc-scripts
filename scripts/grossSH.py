import FITS
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as  misc
from scipy import ndimage
import matplotlib.cm as cm
import pylab
from skimage.draw import ellipse
from skimage.morphology import label
from skimage.measure import regionprops
from scipy.ndimage import geometric_transform

def im2bw(image, threshold):
    (x, y) = image.shape
    image = image/image.max()
    img = np.zeros((x,y))
    for i in range(0,x):
        for j in range(0,y):
            if image[i][j] >= threshold:
                img[i][j] = 1
            else:
                img[i][j] = 0
    return img


data = FITS.Read('myfits.fits')
headers = data[0]
raw_data = data[1]
#print raw_data.mean()
#print raw_data.max()
#print raw_data.min()
#plot
#plt.figure(1)
#plt.subplot(131)
#plt.gca().invert_yaxis()
#plt.imshow(raw_data, cmap=pylab.gray())
tr = 0.42
print tr
raw_data = im2bw(raw_data,tr)
#plot
#plt.figure(2)
#plt.subplot(132)
#plt.gca().invert_yaxis()
#plt.imshow(raw_data, cmap=pylab.gray())

#processed = ndimage.filters.laplace(raw_data,mode='reflect', cval=0.0)
# plot
#plt.figure(3)
#plt.subplot(133)
#plt.gca().invert_yaxis()
#plt.imshow(processed, cmap=pylab.gray())
#plt.show()

label_img = label(raw_data)
#label_img = raw_data.astype(np.int)
#print label_img
# plot
#plt.figure(3)
#plt.subplot(133)
#plt.gca().invert_yaxis()
#plt.imshow(label_img, cmap=pylab.gray())
#plt.show()
props = regionprops(label_img, ['Centroid'])
for i in props:
    x0 = i['Centroid'][0]
    y0 = i['Centroid'][1]
#    plt.plot(x0, y0, 'xr', markersize=8)
print len(props)
#plt.show()

#save it!
#misc.imsave('laplace.jpg', processed)
