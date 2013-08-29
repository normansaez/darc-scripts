#!/usr/bin/env python
'''
Stars
'''

import pygtk
pygtk.require('2.0')
import gtk

from star_coord import star_coord

class Main:
    '''
    Main
    '''
    def __init__(self):
        self.win = gtk.Window()
        self.win.set_size_request(800, 800)
        self.win.set_title('Stars')
        self.win.set_resizable(False)
        self.win.set_events(self.win.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
#        self.win.connect('destroy', gtk.main_quit)
        #self.win.connect('button_press_event', self.show_flower)
       

        self.fix = gtk.Fixed()
        self.win.add(self.fix)
        self.win.show_all()
        img = gtk.Image()
        img.set_from_file('./img/star800.png')
        img.show()
        self.fix.put(img, 0, 0)
        ########################
        self.win2 = gtk.Window()
        self.win2.set_size_request(800, 800)
        self.win2.set_title('Constellations')
        self.win2.set_resizable(False)
        self.win2.set_events(self.win.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        #self.win2.connect('destroy', gtk.main_quit)
        #self.win2.connect('button_press_event', self.show_flower)
       
        self.fix2 = gtk.Fixed()
        self.win2.add(self.fix2)
        self.win2.show_all()
        img2 = gtk.Image()
        img2.set_from_file('./img/deepsky.png')
        img2.show()
        self.fix2.put(img2, 0, 0)

        #Create all buttons here:
        for i in range(1, star_coord.__len__() +1):
            button = gtk.ToggleButton("%d"%i)
            button.connect("toggled", self.callback, "%d"%i)
            button.show()
            self.fix.put(button, star_coord[i][0], star_coord[i][1])

    def callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        star = int(data)
        img = gtk.Image()
        if widget.get_active() is True:
            img.set_from_file('./img/shineStar.png')
        else:
            img.set_from_file('./img/darkStar.png')
        img.show()
        self.fix2.put(img, star_coord[star][0], star_coord[star][1])
        
#    def show_flower(self, widget, event):
#        count = 0
#        if event.type == gtk.gdk.BUTTON_PRESS:
#            count = 1
#        elif event.type == gtk.gdk._2BUTTON_PRESS:
#            count = 2
#        elif event.type == gtk.gdk._3BUTTON_PRESS:
#            count = 3
#
#        for i in range(count):
#            img = gtk.Image()
#            #img.set_from_file('./face-kiss.png')
#            #img.show()
#            x = int(event.x) + (i*self.img_size)
#            y = int(event.y) 
#            coord = """(%d , %d)""" % (x,y)
#            self.label = gtk.Label('X')
#            self.label.modify_fg(gtk.STATE_NORMAL, \
#            gtk.gdk.color_parse('#FFFFFF'))
#            self.label.show()
#            self.fix.put(self.label, x, y)

if __name__ == '__main__':
    app = Main()
    gtk.main()
