import FITS
import numpy as np

data = FITS.Read('myfits.fits')

#data fits  = list
# list[0] = headers
# list[1] = data (numpy.array)
headers = data[0]
raw_data = data[1]

#print headers['parsed']
#y_axis = int(headers['parsed']['NAXIS2'])
#x_axis = int(headers['parsed']['NAXIS1'])

average = np.mean(raw_data)
maxi = raw_data.max()
mini = raw_data.min()

#reshape if is necesarry:
print raw_data.size
print raw_data.ndim
print raw_data.shape
cloned = np.zeros(raw_data.shape)
#raw_data = np.reshape(raw_data, total_size)
#
#count = 0
#for i in cloned:
#    if i > average:
#        cloned_b(count) = 1
#    else:
#        cloned_b(count) = 0
#    count = count + 1 
