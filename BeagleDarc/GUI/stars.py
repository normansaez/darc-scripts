#!/usr/bin/env python

#Kiss
#(c) Noprianto <nop@tedut.com>, 2008, GPL
#

import pygtk
pygtk.require('2.0')
import gtk

class Main:
    def __init__(self):
        self.win = gtk.Window()
        self.win.set_size_request(1148, 566)
        self.win.set_title('Stars')
        self.win.set_resizable(False)
        self.win.set_events(self.win.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.win.connect('destroy', gtk.main_quit)
        self.win.connect('button_press_event', self.show_flower)
       
        self.img_size = 64

        self.fix = gtk.Fixed()
        
        self.win.add(self.fix)

        self.win.show_all()
        img = gtk.Image()
        img.set_from_file('./stars.jpg')
        img.show()
        self.fix.put(img, 0, 0)
        button = gtk.ToggleButton("1")
        button.connect("toggled", self.callback, "1")
        #vbox = gtk.VBox(True, 2)
        #vbox.pack_start(button, True, True, 2)
        button.show()
        self.fix.put(button, 565 , 279)

    def callback(self, widget, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
         
    def show_flower(self, widget, event):
        count = 0
        if event.type == gtk.gdk.BUTTON_PRESS:
            count = 1
            print count
        elif event.type == gtk.gdk._2BUTTON_PRESS:
            count = 2
            print count
        elif event.type == gtk.gdk._3BUTTON_PRESS:
            count = 3
            print count

        for i in range(count):
            img = gtk.Image()
            #img.set_from_file('./face-kiss.png')
            #img.show()
            x = int(event.x) + (i*self.img_size)
            y = int(event.y) 
            coord = "%d , %d" % (x,y)
            #self.fix.put(img, x, y)
            print coord
            self.label = gtk.Label('X')
            self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
            self.label.show()
            self.fix.put(self.label, x, y)

if __name__ == '__main__':
    app = Main()
    gtk.main()
