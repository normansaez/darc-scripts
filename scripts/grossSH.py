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
processed = ndimage.sobel(raw_data, cval=0)
# plot
plt.imshow(processed)
plt.gca().invert_yaxis()
plt.show()
#save it!
scipy.misc.imsave('sobel.jpg', processed)
