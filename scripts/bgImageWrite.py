import FITS
import darc

c=darc.Control("main")
bg = c.Get("bgImage")
data = bg.reshape(480,640)
FITS.Write(data,'backgroundImage20130129.fits',writeMode='a')

