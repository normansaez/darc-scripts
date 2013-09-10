#!/usr/bin/env python
'''
Stars
'''

import os
import pygtk
pygtk.require('2.0')
import gtk

from star_coord import star_coord
from BeagleDarc.Controller import Controller

class Layers:
    '''
    Layers
    '''
    def __init__(self):
        self.path, fil = os.path.split(os.path.abspath(__file__))
        self.win = gtk.Window()
        self.win.set_size_request(800, 800)
        self.win.set_title('Layers')
        self.win.set_resizable(False)
        self.win.set_events(self.win.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.win.connect('destroy', gtk.main_quit)
       

        self.fix = gtk.Fixed()
        self.win.add(self.fix)
        self.win.show_all()

        self.img_ground = gtk.Image()
        self.img_ground.set_from_file(self.path+'/img/ground_layer.png')
        self.fix.put(self.img_ground, 100, 500)
        self.img_ground.show()

        self.img_altitude = gtk.Image()
        self.img_altitude.set_from_file(self.path+'/img/altitude_layer.png')
        self.fix.put(self.img_altitude, 100, 450)
        self.img_altitude.show()
        ############ labels       ##########
        self.label1 = gtk.Label()
        self.label1.set_text("Ground Layer")
        self.label1.show()
        self.fix.put(self.label1, 5, 680)

        self.label2 = gtk.Label()
        self.label2.set_text("Altitude Layer X")
        self.label2.show()
        self.fix.put(self.label2, 5, 580)

        self.label3 = gtk.Label()
        self.label3.set_text("Altitude Layer Y")
        self.label3.show()
        self.fix.put(self.label3, 670, 5)

        ########################
        # ground_scale
        #
        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
        self.ground_scale = gtk.HScale(adjustment)
        self.ground_scale.set_digits(0)
        self.ground_scale.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.ground_scale.connect("value-changed", self.ground_scale_moved)
        self.ground_scale.set_size_request(600, 30)
        self.ground_scale.show()
        self.fix.put(self.ground_scale, 100, 650)
        ########################
        # altitude_scale X
        #
        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
        self.altitude_scale_X = gtk.HScale(adjustment)
        self.altitude_scale_X.set_digits(0)
        self.altitude_scale_X.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.altitude_scale_X.connect("value-changed", self.altitude_scale_X_moved)
        self.altitude_scale_X.set_size_request(600, 30)
        self.altitude_scale_X.show()
        self.fix.put(self.altitude_scale_X, 100, 600)
        ########################
        # altitude_scale Y
        #
        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
        self.altitude_scale_Y = gtk.VScale(adjustment)
        self.altitude_scale_Y.set_digits(0)
        #self.altitude_scale_Y.set_value_pos(gtk.POS_BOTTOM) 
        self.altitude_scale_Y.set_inverted(True)
        self.altitude_scale_Y.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.altitude_scale_Y.connect("value-changed", self.altitude_scale_Y_moved)
        self.altitude_scale_Y.set_size_request(30, 550)
        self.altitude_scale_Y.show()
        self.fix.put(self.altitude_scale_Y, 700, 30)
        # Apply button:
        self.button_ok = gtk.Button("Apply")
        self.button_ok.show()
        self.fix.put(self.button_ok, 700, 750)

        ##Creating controller
        self.controller = Controller()

    def ground_scale_moved(self, event):
        print "ground_scale_moved"
        print self.ground_scale.get_value()
        self.fix.move(self.img_ground, 100+int(self.ground_scale.get_value()*4), 500)

    def altitude_scale_X_moved(self, event):
        print "altitude_scale_X_moved"
        print self.altitude_scale_X.get_value()
        self.fix.move(self.img_altitude, 100+int(self.altitude_scale_X.get_value()*4), 450 - int(self.altitude_scale_Y.get_value()*4))

    def altitude_scale_Y_moved(self, event):
        print "altitude_scale_Y_moved"
        print self.altitude_scale_Y.get_value()
        self.fix.move(self.img_altitude, 100+int(self.altitude_scale_X.get_value()*4), 450 - int(self.altitude_scale_Y.get_value()*4))

if __name__ == '__main__':
    app = Layers()
    gtk.main()
