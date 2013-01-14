import FITS
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import ndimage





data = FITS.Read('myfits.fits')

#data fits  = list
# list[0] = headers
# list[1] = data (numpy.array)
headers = data[0]
raw_data = data[1]


#gettting stats
average = np.mean(raw_data)
maxi = raw_data.max()
mini = raw_data.min()
(y,x) = raw_data.shape
cloned = np.zeros(raw_data.shape)

#reshape if is necesarry:
raw_data = np.reshape(raw_data, raw_data.size)
cloned = np.reshape(cloned,cloned.size)

################################################
count = 0
threshole = average*7.0
print threshole
for i in raw_data:
    if i > threshole:
        cloned[count] = 1
    count = count + 1

################################################
print raw_data.shape
print cloned.shape
print x
print y
#cloned = cloned.reshape(x,y)
#plt.imshow(cloned)
#plt.gca().invert_yaxis()
#plt.show()
FITS.Write(cloned,'myfitsBW.fits')
print "writed"
##################################################
#im = scipy.misc.imread('myfits.fits')
print type(raw_data)
print raw_data.shape
print raw_data.dtype
#raw_1 = raw.astype(np.uint8)
###########
raw_data = raw_data.reshape(y,x)

#processed = ndimage.sobel(raw_data, cval=0.9)
#plt.imshow(processed)
#plt.gca().invert_yaxis()
#plt.show()
#scipy.misc.imsave('sobel.jpg', processed)
processed = ndimage.gaussian_laplace(raw_data, cval=0.1)
#plt.imshow(processed)
#plt.gca().invert_yaxis()
#plt.show()
scipy.misc.imsave('laplace.jpg', processed)

print "finish"
