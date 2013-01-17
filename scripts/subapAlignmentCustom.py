#!/usr/bin/python
import sys
import os
import os.path
import gtk
import numpy
import gobject
import FITS
import controlCorba

class Align:
    def __init__(self,prefix=""):
        self.prefix=prefix
        self.cam=0
        self.ncam=1
        self.win=gtk.Window()
        self.win.set_default_size(480,640)
        self.win.set_title("Subaperture alignment Custom %s on %s"%(prefix,os.environ.get("HOSTNAME","unknown host")))
        self.win.set_icon_from_file(os.path.join(os.path.split(__file__)[0],"logo2.png"))
        self.win.connect("delete-event",self.quit)
        self.unfillSubapLocation={}
        e=gtk.EventBox()
        e.connect("button-press-event",self.clickCanary)
        i=gtk.Image()
        e.add(i)
        i.set_from_file(os.path.join(os.path.split(__file__)[0],"logo2.png"))
        vbox=gtk.VBox()
        self.win.add(vbox)
        hbox=gtk.HBox()
        hbox.add(e)

        vbox.pack_start(hbox,expand=False)
        hbox.pack_start(gtk.Label("Alignment:"),expand=False)
        bget=gtk.Button("Get")
        bget.connect("clicked",self.getAlignment)
        hbox.pack_start(bget)
        bset=gtk.Button("Set")
        bset.connect("clicked",self.setAlignment)
        hbox.pack_start(bset)
        bloa=gtk.Button("Load")
        bloa.connect("clicked",self.loadAlignment)
        hbox.pack_start(bloa)
        bsav=gtk.Button("Save")
        bsav.connect("clicked",self.saveAlignment)
        hbox.pack_start(bsav)
        b=gtk.Button("Show")
        b.connect("clicked",self.showAlignment)
        hbox.pack_start(b)
        hbox=gtk.HBox()
        vbox.pack_start(hbox,expand=False)
        hbox.pack_start(gtk.Label("Cam:"),expand=False)
        s=gtk.SpinButton()
        s.set_value(0)
        s.set_width_chars(1)
        s.connect("value-changed",self.changeCam)
        a=s.get_adjustment()
        a.set_value(0)
        a.set_upper(self.ncam-1)
        self.adjustment=a
        a.set_lower(0)
        a.set_page_increment(1)
        a.set_step_increment(1)
        hbox.pack_start(s,expand=False)
        self.coordsLabel=gtk.Label()
        hbox.pack_start(self.coordsLabel)
        hbox=gtk.HBox()
        vbox.pack_start(hbox,expand=False)
        bx=gtk.Button("Move X")
        bx.connect("clicked",self.moveX)
        hbox.pack_start(bx)
        self.ex=gtk.Entry()
        self.ex.set_text("1")
        self.ex.set_width_chars(2)
        hbox.pack_start(self.ex)
        by=gtk.Button("Move Y")
        by.connect("clicked",self.moveY)
        hbox.pack_start(by)
        self.ey=gtk.Entry()
        self.ey.set_width_chars(2)
        self.ey.set_text("1")
        hbox.pack_start(self.ey)
        bsx=gtk.Button("Inc X size")
        bsx.connect("clicked",self.incsizeX)
        hbox.pack_start(bsx)
        self.esx=gtk.Entry()
        self.esx.set_width_chars(2)
        self.esx.set_text("1")
        hbox.pack_start(self.esx)
        bsy=gtk.Button("Inc Y size")
        bsy.connect("clicked",self.incsizeY)
        hbox.pack_start(bsy)
        self.esy=gtk.Entry()
        self.esy.set_width_chars(2)
        self.esy.set_text("1")
        hbox.pack_start(self.esy)

        bsx=gtk.Button("Set size X")
        bsx.connect("clicked",self.setsizeX)
        hbox.pack_start(bsx)
        self.essx=gtk.Entry()
        self.essx.set_width_chars(2)
        self.essx.set_text("1")
        hbox.pack_start(self.essx)
        bsy=gtk.Button("Set size Y")
        bsy.connect("clicked",self.setsizeY)
        hbox.pack_start(bsy)
        self.essy=gtk.Entry()
        self.essy.set_width_chars(2)
        self.essy.set_text("1")
        hbox.pack_start(self.essy)

        h=gtk.HBox()
        vbox.pack_start(h,expand=False)
        h.add(gtk.Label("Warning: Upside down relative to darcplot"))
        b=gtk.Button("Compute filling subaps")
        b.connect("clicked",self.computeFilling)
        h.add(b)
        b=gtk.Button("Unfill")
        b.connect("clicked",self.unfill)
        h.add(b)
        


        self.img=gtk.Image()
        self.img.set_alignment(0,0)
        self.img.set_padding(0,0)
        self.event=gtk.EventBox()
        self.event.connect("button-press-event",self.click)
        self.event.connect("button-release-event",self.unclick)
        self.event.connect("motion-notify-event",self.motion)
        self.event.connect("key-press-event",self.keypress)
        #self.event.connect("expose-event",self.expose)
        self.pixbuf=gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,256,256)
        s=gtk.ScrolledWindow()
        s.add_with_viewport(self.event)
        vbox.pack_start(s)
        #vbox.pack_start(self.event)
        self.event.add(self.img)
        self.win.show_all()
        self.img.set_from_pixbuf(self.pixbuf)
        self.img.queue_draw()
        self.getAlignment()
        #gobject.idle_add(self.newimg)
    # def expose(self,w=None,e=None):
    #     print "Expose"
    #     pass

    def changeCam(self,w):
        self.cam=w.get_value_as_int()
        if self.cam>=self.ncam:
            self.cam=self.ncam-1
        if self.cam<0:
            self.cam=0
        print self.cam
        self.draw()

    def computeFilling(self,w):
        s=self.makeSubapLocation()
        if self.unfillSubapLocation.get(self.cam)==None:
            FITS.Write(s,"unfillSubapLocation%d.fits"%self.cam)
            self.unfillSubapLocation[self.cam]=s
        #Now, get used subaps etc.
        # c=controlCorba.controlClient(self.prefix)
        # subflag=c.Get("subapFlag")
        # npxlx=c.Get("npxlx")
        # npxly=c.Get("npxly")
        subflag,subapLocation,selected=self.getPointers()
        npxlx=self.npxlx[self.cam]
        npxly=self.npxly[self.cam]
        nsubapsUsed=subflag.sum()
        nx=int(numpy.ceil(numpy.sqrt(nsubapsUsed)))
        ny=(nsubapsUsed+nx-1)//nx
        #nx and ny tells us the grid on which to place subaps...
        sl=numpy.zeros((subflag.size,6),numpy.int32)
        pos=0
        row=0
        col=0
        ysp=(npxly+ny-1)//ny
        xsp=(npxlx+nx-1)//nx
        for i in range(subflag.size):
            if subflag[i]:#a used subap
                if row==ny-1 and col==0:#last row...
                    #How many are in the last row?
                    nlast=nsubapsUsed-(ny-1)*nx
                    xsp=(npxlx+nlast-1)//nlast
                yto=(row+1)*ysp
                if yto>npxly:
                    yto=npxly
                xto=(col+1)*xsp
                if xto>npxlx:
                    xto=npxlx
                sl[pos]=(row*ysp,yto,1,col*xsp,xto,1)
                pos+=1
                col+=1
                if col==nx:#wrap around
                    col=0
                    row+=1
        subapLocation[:]=sl*2
        self.draw()

    def unfill(self,w):
        if self.unfillSubapLocation.get(self.cam)==None:
            if os.path.exists("unfillSubapLocation%d.fits"%self.cam):
                sl=FITS.Read("unfillSubapLocation%d.fits"%self.cam)[1]
            else:
                print "Couldn't find file unfillSubapLocation%d.fits"%self.cam
        else:
            sl=self.unfillSubapLocation[self.cam]
            self.unfillSubapLocation[self.cam]=None

        subflag,subapLocation,selected=self.getPointers()
        subapLocation[:]=sl*2
        self.draw()

    def moveX(self,b):
        """Move all selected subaps in x direction"""
        try:
            val=int(self.ex.get_text())
        except:
            val=1
        val*=2
        subflag,subapLocation,selected=self.getPointers()
        for i in range(subapLocation.shape[0]):
            if subflag[i] and selected[i]:
                subapLocation[i,3:5]+=val
        self.draw()
    def moveY(self,b):
        """Move all selected subaps in x direction"""
        try:
            val=int(self.ey.get_text())
        except:
            val=1
        val*=2
        subflag,subapLocation,selected=self.getPointers()
        for i in range(subapLocation.shape[0]):
            if subflag[i] and selected[i]:
                subapLocation[i,0:2]+=val
        self.draw()
    def incsizeX(self,b):
        """Move all selected subaps in x direction"""
        try:
            val=int(self.esx.get_text())
        except:
            val=1
        val*=2
        subflag,subapLocation,selected=self.getPointers()
        for i in range(subapLocation.shape[0]):
            if subflag[i] and selected[i]:
                subapLocation[i,4]+=val
        self.draw()
    def incsizeY(self,b):
        """Move all selected subaps in x direction"""
        try:
            val=int(self.esy.get_text())
        except:
            val=1
        val*=2
        subflag,subapLocation,selected=self.getPointers()
        for i in range(subapLocation.shape[0]):
            if subflag[i] and selected[i]:
                subapLocation[i,1]+=val
        self.draw()
    def setsizeX(self,b):
        """Set x size of subaps"""
        try:
            val=int(self.essx.get_text())
        except:
            val=1
        val*=2
        subflag,subapLocation,selected=self.getPointers()
        for i in range(subapLocation.shape[0]):
            if subflag[i] and selected[i]:
                subapLocation[i,4]=subapLocation[i,3]+val
        self.draw()
    def setsizeY(self,b):
        """Set y size of subaps"""
        try:
            val=int(self.essy.get_text())
        except:
            val=1
        val*=2
        subflag,subapLocation,selected=self.getPointers()
        for i in range(subapLocation.shape[0]):
            if subflag[i] and selected[i]:
                subapLocation[i,1]=subapLocation[i,0]+val
        self.draw()
        
    def getPointers(self):
        s=self.nsub[:self.cam].sum()
        e=s+self.nsub[self.cam]
        subflag=self.subflag[s:e]
        #soff=self.subflag[:self.nsub[:self.cam].sum()].sum()
        subapLocation=self.subapLocation[s:e]#off:soff+subflag.sum()]
        selected=self.selected[s:e]#off:soff+subflag.sum()]
        return subflag,subapLocation,selected

    def draw(self):
        # subflag=self.subflag[self.nsub[:self.cam].sum():self.nsub[:self.cam+1].sum()]
        # soff=self.subflag[:self.nsub[:self.cam].sum()].sum()
        # subapLocation=self.subapLocation[soff:soff+subflag.sum()]
        # selected=self.selected[soff:soff+subflag.sum()]
        subflag,subapLocation,selected=self.getPointers()
                                         
        self.arr[:]=0xff
        red=(0xff,0,0)
        green=(0,0xff,0)
        for i in range(subapLocation.shape[0]):
            if subflag[i]:
                s=subapLocation[i]
                while s[0]<0:
                    s[:2]+=1
                while s[1]>self.npxly[self.cam]*2:#pixbuf.get_height():
                    s[:2]-=1
                while s[3]<0:
                    s[3:5]+=1
                while s[4]>self.npxlx[self.cam]*2:#pixbuf.get_width():
                    s[3:5]-=1
                self.arr[s[0],s[3]:s[4]]=red
                self.arr[s[1]-1,s[3]:s[4]]=red
                self.arr[s[0]:s[1],s[3]]=red
                self.arr[s[0]:s[1],s[4]-1]=red
                if selected[i]:
                    self.arr[s[0]+1:s[1]-1,s[3]+1:s[4]-1]=green
        self.img.queue_draw()
        
    def clickCanary(self,w=None,e=None):
        subflag,subapLocation,selected=self.getPointers()
        green=(0,0xff,0)
        white=(0xff,0xff,0xff)
        if numpy.any(selected):
            selected[:]=0
            col=white
        else:
            selected[:]=1
            col=green
        for i in range(subapLocation.shape[0]):
            if subflag[i]:
                s=subapLocation[i]
                self.arr[s[0]+1:s[1]-1,s[3]+1:s[4]-1]=col
        self.img.queue_draw()

    def keypress(self,w=None,e=None):
        print w,e
    def click(self,w=None,e=None):
        #print e.button,dir(e),e.x,e.y
        #Are we in a subap?
        #If so, select or deselect the subap, and fill colour it.
        subflag,subapLocation,selected=self.getPointers()
        update=0
        green=(0,0xff,0)
        white=(0xff,0xff,0xff)
        for i in range(subapLocation.shape[0]):
            if subflag[i]:
                s=subapLocation[i]
                if e.x>s[3] and e.x<s[4] and e.y>s[0] and e.y<s[1]:
                    update=1
                    selected[i]=1-selected[i]
                    if selected[i]:
                        self.arr[s[0]+1:s[1]-1,s[3]+1:s[4]-1]=green
                    else:
                        self.arr[s[0]+1:s[1]-1,s[3]+1:s[4]-1]=white

                    self.coordsLabel.set_text("y%d-%d,x%d-%d"%(s[0]/2,s[1]/2,s[3]/2,s[4]/2))
                    break
        if update:
            self.img.queue_draw()
        return True

    def unclick(self,w=None,e=None):
        #print e.button,dir(e),e.x,e.y
        return True
    def motion(self,w,e):
        #print e.x,e.y
        return True
    # def newimg(self,w=None,a=None):
    #     arr=self.pixbuf.get_pixels_array()
    #     arr[:]=self.rand[self.cnt]
    #     #self.pixbuf.pixel_array[:]=self.rand[self.cnt]#(numpy.random.random(self.pixbuf.pixel_array.shape)*100).astype(self.pixbuf.pixel_array.dtype)
    #     self.cnt+=1
    #     if self.cnt>=self.rand.shape[0]:
    #         self.cnt=0
    #     self.img.queue_draw()
    #     return True
    def getAlignment(self,w=None):
        if type(w)==type(""):
            data=FITS.Read(w)
            subapLocation=data[1]
            self.npxlx=numpy.array(eval(data[0]["parsed"]["npxlx"]))
            self.npxly=numpy.array(eval(data[0]["parsed"]["npxly"]))
            self.nsub=numpy.array(eval(data[0]["parsed"]["nsub"]))
            self.subflag=data[3]
        else:
            c=controlCorba.controlClient(self.prefix)
            subapLocation=c.Get("subapLocation")
            subapLocation.shape=subapLocation.size/6,6
            self.subflag=c.Get("subapFlag")
            self.nsub=c.Get("nsub")
            self.npxlx=c.Get("npxlx")
            self.npxly=c.Get("npxly")
        self.ncam=self.nsub.size
        self.adjustment.set_upper(self.ncam-1)

        self.orig=subapLocation.copy()
        self.pixbuf=gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,self.npxlx[self.cam]*2,self.npxly[self.cam]*2)
        
        self.arr=self.pixbuf.get_pixels_array()
        self.arr[:]=0xff
        self.img.set_from_pixbuf(self.pixbuf)

        subapLocation=self.subapToSingle(subapLocation)
        subapLocation*=2
        self.subapLocation=subapLocation
        self.selected=numpy.ones((self.subapLocation.shape[0],),numpy.int8)
        self.draw()

    def setAlignment(self,w):
        c=controlCorba.controlClient(self.prefix)
        s=self.makeSubapLocation(allcam=1)
        pxlcnt=self.count(s)
        c.set("subapLocation",s,swap=0)
        c.set("subapFlag",self.subflag,swap=0)
        c.set("pxlCnt",pxlcnt)
    def saveAlignment(self,w):
        s=self.makeSubapLocation(allcam=1)
        print numpy.alltrue(s==self.orig)
        fname="%ssubapLocation.fits"%self.prefix
        FITS.Write(s,fname,extraHeader=["npxlx   = '%s'"%str(list(self.npxlx)),"npxly   = '%s'"%str(list(self.npxly)),"nsub    = '%s'"%str(list(self.nsub))])
        FITS.Write(self.subflag,fname,writeMode='a')
        self.coordsLabel.set_text("Written to %s"%fname)
    def loadAlignment(self,w):
        fname="%ssubapLocation.fits"%self.prefix
        self.getAlignment(fname)
    def showAlignment(self,w):
        s=self.makeSubapLocation()
        w=gtk.Window()
        l=gtk.Label(str(s))
        w.add(l)
        w.show_all()
    def quit(self,w=None,a=None):
        gtk.main_quit()

    def subapToSingle(self,subapLocation):
        """Convert into a single camera image"""
        if self.npxlx.size==2:#2 camera system
            #raise Exception("Not yet configured for andorgated")
            return subapLocation
        else:
            return subapLocation

    def count(self,s):
        pxlcnt=numpy.zeros((s.shape[0],),numpy.int32)
        pos=0
        spos=0
        for k in range(self.ncam):
            for i in range(self.nsub[k]):
                if self.subflag[pos]:
                    pxlcnt[pos]=(s[pos,1]-1)*self.npxlx[k]+s[pos,4]
                else:
                    pxlcnt[pos]=-256
                pos+=1
        return pxlcnt


    def makeSubapLocation(self,allcam=0):
        if allcam:
            subapLocation=self.subapLocation
        else:
            subflag,subapLocation,selected=self.getPointers()
        return subapLocation/2

if __name__=="__main__":
    prefix="main"
    if len(sys.argv)>1:
        prefix=sys.argv[1]
    numpy.set_printoptions(threshold=10000)
    img=Align(prefix)
    gtk.main()
