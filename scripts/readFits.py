import FITS
import matplotlib.pyplot as plt
import pylab

#data = FITS.Read('mainsubapLocationSCAO1_121121.fits')
data = FITS.Read('newSubAp.fits')
headers  = data[0]
raw_data = data[1]

#parsed, raw data
print headers['parsed']
for key in headers['parsed']:
    print  "%s -> %s" % (key,headers['parsed'][key])

npxlx = eval(headers['parsed']['npxlx'])[0]
npxly = eval(headers['parsed']['npxly'])[0]

print raw_data.size
print raw_data.shape
print raw_data.dtype
print raw_data
print "--------------"
y_start = raw_data[:,0]
y_end   = raw_data[:,1]
y_step  = raw_data[:,2]
x_start = raw_data[:,3]
x_end   = raw_data[:,4]
x_step  = raw_data[:,5]

plt.plot(x_start,y_start,'xr')
plt.plot(x_end,y_end,'og')
plt.show()

#plt.imshow(raw_data, cmap=pylab.gray())
#plt.gca().invert_yaxis()
#plt.show()

#img = raw_data.reshape((npxlx,npxly))

