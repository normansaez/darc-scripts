#!/usr/bin/env python
import os
import sys
import socket
import time
import glob
import numpy
import gtk
import darc
import FITS
import correlation
import calibrate
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import pylab


"""Order to call:
getImg
plotImg
makefft
getSlopes

add to current ref

set in darc, and set corr.
"""



def getImg(nfr):
    d=darc.Control("main")
    img=d.SumData("rtcCalPxlBuf",nfr)[0]/nfr
    return img

def plotImg(img):
    import gist
    im=img[256*256:]
    im.shape=128,128
    gist.fma()
    gist.pli(im)

def setCorr(val=1):
    cm=numpy.zeros((49*5),"i")
    cm[-49:]=val
    d=darc.Control("main")
    d.Set("centroidMode",cm)

def makefft(img,pad=0):
    d=darc.Control("main")
    return correlation.transformPSF(img,3,[256,256,128],[128]*3,[98,98,49],d.Get("subapLocation"),d.Get("subapFlag"),pad)

def makeIdent(npxlx=None,npxly=None,sl=None):
    d=darc.Control("main")
    nsub=[98,98,49]
    sf=d.Get("subapFlag")
    if npxlx==None:
        npxlx=d.Get("npxlx")
    if npxly==None:
        npxly=d.Get("npxly")
    if sl==None:
        sl=d.Get("subapLocation")
    ident=correlation.generateIdentityCorr(npxlx,npxly,nsub,sf,sl)
    return ident

def getCurrentImg():
    d=darc.Control("main")
    fft=d.Get("corrFFTPattern")
    if fft==None:
        img=correlation.generateIdentityCorr(d.Get("npxlx"),d.Get("npxly"),d.Get("nsub"),d.Get("subapFlag"),d.Get("subapLocation"))
    else:
        try:
            npxlx=d.Get("corrNpxlx")
        except:
            npxlx=d.Get("npxlx")
        try:
            npxly=d.Get("corrNpxly")
        except:
            npxly=d.Get("npxly")
        try:
            npxlcum=d.Get("corrNpxlCum")
        except:
            npxlcum=numpy.insert(numpy.cumsum(npxlx*npxly),0,0)
        try:
            sl=d.Get("corrSubapLoc")
        except:
            sl=d.Get("subapLocation")
        nsub=d.Get("nsub")
        sf=d.Get("subapFlag")
        img=correlation.untransformPSF(fft,3,npxlx,npxly,nsub,sl,sf)
        sl2=d.Get("subapLocation")
        npxlx2=d.Get("npxlx")
        npxly2=d.Get("npxly")
        img=correlation.unpackImg(img,3,nsub,sf,npxlx,npxly,sl,npxlx2,npxly2,sl2)
    return img

def getSlopes(img,pad=0,retcorr=0):
    """Computes slopes if img is used as a correlation image"""
    d=darc.Control("main")
    cm=d.Get("centroidMode")
    if type(cm)==numpy.ndarray and numpy.any(cm[-49:]):#in correlation mode.
        cur=getCurrentImg()
        usenow=1
    else:
        cur=makeIdent()
        usenow=0
    sf=d.Get("subapFlag")
    nsub=d.Get("nsub")
    corr=correlation.makeCorrelation(img,cur,3,d.Get("npxlx"),d.Get("npxly"),nsub,d.Get("subapLocation"),sf,pad)

    slopes=calibrate.makeSlopes(corr["correlation"],3,nsub,corr["corrNpxlx"],corr["corrNpxly"],sf,corr["corrSubapLoc"])
    slopes-=0.5#correlation is pixel centred, not 2x2 centred.
    slopes[:288]=0#not using NGS
    if retcorr:
        return slopes,usenow,corr
    else:
        return slopes,usenow


class Correl:
    def __init__(self,w=None):
        self.prefix="main"
        if w==None:
            self.win=gtk.Window()
            self.win.set_title("LGS correlation tool for CANARY on %s"%socket.gethostname())
            self.win.set_icon_from_file(os.path.join(os.path.split(__file__)[0],"canaryIcon.png"))
            self.win.connect("delete-event",self.quit)
        else:
            self.win=w
        self.img=None
        self.pad=0
        self.hbox=gtk.HBox()
        vbox=gtk.VBox()
        self.win.add(self.hbox)
        self.hbox.pack_start(vbox,False)
        h=gtk.HBox()
        vbox.pack_start(h,False)
        i=gtk.Image()
        i.set_from_file(os.path.join(os.path.split(__file__)[0],"canaryLogo.png"))
        h.pack_start(i,False)
        b=gtk.Button("Grab")
        b.set_tooltip_text("Grab calibrated images")
        h.pack_start(b,False)
        e=gtk.Entry()
        e.set_width_chars(4)
        e.set_text("100")
        e.set_tooltip_text("Number of frames to average")
        h.pack_start(e,False)
        b.connect("clicked",self.grab,e)
        b=gtk.Button("Update")
        b.set_tooltip_text("Gets current darc state")
        b.connect("clicked",self.update)
        h.pack_start(b,False)
        b=gtk.Button("Reset")
        b.set_tooltip_text("Resets to CoG, refslopes to 0")
        b.connect("clicked",self.reset)
        h.pack_start(b,False)
        h=gtk.HBox()
        vbox.pack_start(h,False)
        b=gtk.Button("Save ref")
        b.set_tooltip_text("Gets ref slopes from darc and saves")
        b.connect("clicked",self.saveRef)
        h.pack_start(b,False)
        e=gtk.Entry()
        e.set_width_chars(10)
        if os.path.exists("/Canary"):
            e.set_text("/Canary/data/")
        else:
            e.set_text("data/")
        e.set_tooltip_text("Directory for ref slopes")
        self.dataDirEntry=e
        h.pack_start(e,True)
        h=gtk.HBox()
        vbox.pack_start(h,False)
        b=gtk.Button("Load")
        b.set_tooltip_text("Loads ref slopes and sets in darc")
        b.connect("clicked",self.loadRef)
        h.pack_start(b,False)
        e=gtk.Entry()
        e.set_width_chars(10)
        e.set_tooltip_text("Filename for loading ref slopes")
        self.entrySlopesFilename=e
        h.pack_start(e,True)

        h=gtk.HBox()
        vbox.pack_start(h,False)
        b=gtk.Button("Compute slopes")
        b.set_tooltip_text("Computes slopes related to this image")
        h.pack_start(gtk.Label("Padding:"),False)
        e=gtk.Entry()
        e.set_width_chars(4)
        e.set_text("8")
        e.set_tooltip_text("FFT padding")
        self.entryPad=e
        h.pack_start(e,False)
        b.connect("clicked",self.computeSlopes,e)
        h.pack_start(b,False)
        b=gtk.Button("RTD")
        b.set_tooltip_text("Start a RTD looking at correlation (this will need restarting if padding changes)")
        b.connect("clicked",self.rtd)
        h.pack_start(b,False)
        h=gtk.HBox()
        vbox.pack_start(h,False)
        b=gtk.Button("Upload img")
        b.set_tooltip_text("upload the correlation image (but don't change centroiding mode")
        b.connect("clicked",self.upload,e)
        h.pack_start(b,False)

        b=gtk.RadioButton(None,"Set to CoG")
        self.setCoGButton=b
        b.set_tooltip_text("Set to CoG mode, will restore ref slopes to CoG slopes.")
        self.setCoGHandle=b.connect("toggled",self.setCoG,e)
        h.pack_start(b,False)
        b=gtk.RadioButton(b,"Set to Corr")
        self.setCorrButton=b
        b.set_tooltip_text("Set to Correlation mode (LGS only).  Updates ref slopes.  Doesn't upload new correlation image.")
        h.pack_start(b,False)


        fig1=Figure()
        self.fig1=FigureCanvas(fig1)
        self.fig1.set_size_request(300,300)
        self.im=fig1.add_subplot(2,1,1)
        self.im2=fig1.add_subplot(2,1,2)
        self.hbox.pack_start(self.fig1,True)
        
        vbox.pack_start(gtk.Label("""Instructions: Click "update".
Grab some data by clicking grab. This is
calibrated pixels.  Choose your padding and
compute slopes.  Then upload img.  Then set
to correlation.  This should automagically
update the refslopes so that the AO
correction should be unaffected.
When you want to update the correlation
image, grab some more data, click compute
slopes and then upload img.  This can be
done when already in correlation mode.  It
will update the ref slopes as necessary.
When finished, go back to CoG mode, and
you should find the ref slopes are 
returned to what they were at the start 
(with maybe slight differences due to
floating point rounding error).
Clicking reset sets to CoG, and zeros the
ref slopes.  Clicking load will load the
ref slopes from disk and set in darc.  
Save will save the ref slopes (so do this
at the start).
Padding should be such that fft wrapping
doesn't occur in the RTD image"""),False)

        self.win.show_all()
    def quit(self,w,e=None):
        gtk.main_quit()
    def grab(self,w,e):
        nfr=int(e.get_text())
        self.img=getImg(nfr)
        img=self.img[256**2:]
        img.shape=128,128
        self.im.cla()
        self.im.set_title("rtcCalPxlBuf")
        self.im.imshow(img)
        self.fig1.draw()

    def update(self,w):
        d=darc.Control(self.prefix)
        cm=d.Get("centroidMode")
        if type(cm)==numpy.ndarray and numpy.any(cm[-49:]):#in correlation mode.
            cur=getCurrentImg()
            cog=0
            print "In correlation mode"
        else:
            cur=makeIdent()
            cog=1
            print "In CoG mode"
        self.setCoGButton.handler_block(self.setCoGHandle)
        if cog:
            self.setCoGButton.set_active(True)
        else:
            self.setCorrButton.set_active(True)
        self.setCoGButton.handler_unblock(self.setCoGHandle)
        self.img=getCurrentImg()
        print self.img.shape
        img=self.img[256**2:]
        img.shape=128,128
        self.im.cla()
        self.im.set_title("Currently used image")
        self.im.imshow(img)
        self.fig1.draw()
        #self.computeSlopes(None,self.entryPad)

    def reset(self,w):
        d=darc.Control(self.prefix)
        d.Set(["centroidMode","refCentroids","corrFFTPattern","corrSubapLoc","corrNpxlx","corrNpxlCum"],["CoG",None,None,None,d.Get("npxlx"),numpy.insert(numpy.cumsum(d.Get("npxlx")*d.Get("npxly")),0,0).astype(numpy.int32)])

    def makefilename(self,dironly=0):
        fdir=self.dataDirEntry.get_text()
        if not os.path.exists(fdir):
            rel=""
            if fdir[0]=='/':
                rel="/"
            dirs=fdir.split("/")
            for d in dirs:
                rel+=d+"/"
                if not os.path.exists(rel):
                    print "Making directory %s"%rel
                    os.mkdir(rel)
        if dironly:
            return fdir
        else:
            return os.path.join(fdir,"corr"+time.strftime("%y%m%d_%H%M%S_"))

    def saveRef(self,w):
        d=darc.Control(self.prefix)
        rf=d.Get("refCentroids")
        if rf!=None:
            fn=self.makefilename()
            fn2=fn+self.prefix+"refCentroids.fits"
            FITS.Write(rf,fn2)
            self.entrySlopesFilename.set_text(os.path.split(fn2)[1])
        else:
            print "No ref slopes to save"
    def loadRef(self,w):
        dd=self.makefilename(dironly=1)
        e=self.entrySlopesFilename
        fname=e.get_text()
        if len(fname)==0:
            fname=None
        else:
            fname=os.path.join(dd,fname)
            flist=glob.glob(fname)
            flist.sort()
            if len(flist)==0:
                #file selection
                fname=None
            else:
                fname=flist[-1]#chose latest.
                e.set_text(os.path.split(fname)[1])
        if fname==None:
            #pop up file selection.
            f=gtk.FileChooserDialog("Load ref slopes",self.win,action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT,gtk.STOCK_OK,gtk.RESPONSE_ACCEPT))
            f.set_current_folder(dd)
            f.set_modal(True)
            fil=gtk.FileFilter()
            fil.set_name("Ref slopes files")
            fil.add_pattern("corr*_*_*refCentroids.fits")
            f.add_filter(fil)
            f.set_filter(fil)
            fil=gtk.FileFilter()
            fil.set_name("All files")
            fil.add_pattern("*")
            f.add_filter(fil)
            resp=f.run()
            if resp==gtk.RESPONSE_ACCEPT:
                fname=f.get_filename()
            f.destroy()
        if fname!=None:
            print "Reading %s"%fname
            data=FITS.Read(fname)[1]
            d=darc.Control(self.prefix)
            d.Set("refCentroids",data)
            self.entrySlopesFilename.set_text(os.path.split(fname)[1])

    def computeSlopes(self,w,e):
        pad=int(e.get_text())
        self.newslopes,usernow,self.corr=getSlopes(self.img,pad,1)
        img=self.corr["correlation"]
        img=img[self.corr["corrNpxlCum"][2]:]
        img.shape=self.corr["corrNpxly"][2],self.corr["corrNpxlx"][2]
        self.pad=pad
        self.im.cla()
        self.im.set_title("Correlated img")
        self.im.imshow(img)
        self.im2.cla()
        self.im2.set_title("Update to slopes")
        self.im2.plot(self.newslopes[288:])
        self.fig1.draw()
        
    def upload(self,w,e):
        pad=int(e.get_text())
        if pad!=self.pad:
            self.computeSlopes(None,e)
            d=gtk.Dialog("Padding changed",self.win,gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT,gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            d.vbox.pack_start(gtk.Label("Padding has changed since you last computed slopes.\nThese have been recomputed for you to check.\nClick OK to continue."))
            d.show_all()
            resp=d.run()
            d.destroy()
            if resp==gtk.RESPONSE_ACCEPT:
                self.pad=pad
        if self.pad==pad:
            newslopes,usenow=getSlopes(self.img,pad)
            newcorr=makefft(self.img,pad)
            d=darc.Control(self.prefix)
            if usenow:#currently in corr mode, so update the slopes...
                refSlopes=d.Get("refCentroids")
                if refSlopes==None:
                    refSlopes=-newslopes
                else:
                    refSlopes-=newslopes
                newcorr["refCentroids"]=refSlopes
            d.Set(newcorr.keys(),newcorr.values())
    def setCoG(self,w,e):
        d=darc.Control(self.prefix)
        if w.get_active():
            #has set to cog mode.  So change back to cog mode.
            cm=numpy.zeros((49*5,),numpy.int32)
            #so get current correlation image, and compute the ref slopes offset.
            img=makeIdent()
            #compute padding currently used.
            sl=d.Get("subapLocation")
            try:
                sl2=d.Get("corrSubapLoc")
            except:
                sl2=sl.copy()
            sl.shape=sl.size//6,6
            sl2.shape=sl2.size//6,6
            padarr=(sl2[:,1::3]-sl2[:,::3])/numpy.where(sl2[:,2::3]==0,1000,sl2[:,2::3])-(sl[:,1::3]-sl[:,::3])/numpy.where(sl[:,2::3]==0,1000,sl[:,2::3])
            padused=numpy.max(padarr)//2
            print "Calculated currently used padding as %d"%padused
            slopes,usenow=getSlopes(img,padused)
            refSlopes=d.Get("refCentroids")
            if refSlopes==None:
                refSlopes=-slopes
            else:
                refSlopes-=slopes
            d.Set(["centroidMode","refCentroids"],[cm,refSlopes])
        else:
            #has set to corr mode (but currently in cog mode).
            img=getCurrentImg()
            slopes,usenow=getSlopes(img,self.pad)
            refSlopes=d.Get("refCentroids")
            if refSlopes==None:
                refSlopes=-slopes
            else:
                refSlopes-=slopes
            cm=numpy.zeros((49*5,),numpy.int32)
            cm[-49:]=1
            d.Set(["centroidMode","refCentroids"],[cm,refSlopes])

    def rtd(self,w):
        d=darc.Control(self.prefix)
        try:
            npxlx=d.Get("corrNpxlx")
        except:
            npxlx=d.Get("npxlx")
        try:
            npxly=d.Get("corrNpxly")
        except:
            npxly=d.Get("npxly")
        off=(npxlx*npxly)[:-1].sum()
        os.system("""darcplot --prefix=main rtcCorrBuf 25 "-mdata=data[%d:];data.shape=%d,%d" &"""%(off,npxly[-1],npxlx[-1])) 
        

if __name__=="__main__":
    c=Correl()
    gtk.main()
