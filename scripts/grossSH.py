import FITS
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as  misc
from scipy import ndimage
import matplotlib.cm as cm
import pylab

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
#data fits  = list
# list[0] = headers
# list[1] = data (numpy.array)
headers = data[0]
raw_data = data[1]

#plot
plt.figure(1)
#plt.subplot(131)
plt.imshow(raw_data, cmap=pylab.gray())
plt.gca().invert_yaxis()

raw_data = im2bw(raw_data,0.4)
plt.figure(2)
#plt.subplot(132)
plt.imshow(raw_data, cmap=pylab.gray())
plt.gca().invert_yaxis()
#print raw_data
#print raw_data.max()
#print raw_data.min()
processed = ndimage.filters.laplace(raw_data,mode='reflect', cval=0.0)
# plot
plt.figure(3)
#plt.subplot(133)
plt.imshow(processed, cmap=pylab.gray())
plt.gca().invert_yaxis()
plt.show()
#save it!
misc.imsave('laplace.jpg', processed)
