import numpy as np
from math import radians
from math import sin
from math import cos
from math import floor
import matplotlib.pyplot as plt 

import FITS
import pylab
from skimage.draw import ellipse
from skimage.morphology import label
from skimage.measure import regionprops
from scipy.ndimage import geometric_transform

circle = np.zeros((10,10),dtype=int)

x = 5
y = 5
r = 3
for i in range(0,361):
    angle = radians(i)
    a = floor(r*cos(angle)+x)
    b = floor(r*sin(angle)+y)
    circle[a][b] = 1

plt.imshow(circle, cmap=pylab.gray())
plt.show()

print circle
#label_img = label(circle)
label_img = circle
#print label_img
props = regionprops(label_img, ['BoundingBox','Centroid','Orientation','MajorAxisLength','MinorAxisLength'])

for i in props:
    x0 = i['Centroid'][0]
    y0 = i['Centroid'][1]
    plt.plot(x0, y0, '.g', markersize=15)
    print "%f, %f" % (x0,y0)
print len(props)
plt.show()

