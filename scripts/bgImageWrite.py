import FITS
import darc

c=darc.Control("main")
bg = c.Get("bgImage")
data = bg.reshape(480,640)
FITS.Write(data,'spot1.fits',writeMode='a')

