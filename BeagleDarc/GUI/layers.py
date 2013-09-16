#!/usr/bin/env python
'''
Stars
'''

import os
import pygtk
pygtk.require('2.0')
import gtk
import pango 

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

        # ground: sts init
        self.sts_ground_init = gtk.Image()
        self.sts_ground_init.set_from_file(self.path+'/img/led-green.gif')
        self.fix.put(self.sts_ground_init, 135, 695)
        self.sts_ground_init.show()

        # ground: sts end
        self.sts_ground_end = gtk.Image()
        self.sts_ground_end.set_from_file(self.path+'/img/led-green.gif')
        self.fix.put(self.sts_ground_end, 650, 695)
        self.sts_ground_end.show()

        # altitude X : sts init
        self.sts_altitude_X_init = gtk.Image()
        self.sts_altitude_X_init.set_from_file(self.path+'/img/led-green.gif')
        self.fix.put(self.sts_altitude_X_init, 135, 615)
        self.sts_altitude_X_init.show()

        # altitude X : sts end
        self.sts_altitude_X_end = gtk.Image()
        self.sts_altitude_X_end.set_from_file(self.path+'/img/led-green.gif')
        self.fix.put(self.sts_altitude_X_end, 650, 615)
        self.sts_altitude_X_end.show()

        # altitude Y : sts init
        self.sts_altitude_Y_init = gtk.Image()
        self.sts_altitude_Y_init.set_from_file(self.path+'/img/led-green.gif')
        self.fix.put(self.sts_altitude_Y_init, 705, 15)
        self.sts_altitude_Y_init.show()

        # altitude Y : sts end
        self.sts_altitude_Y_end = gtk.Image()
        self.sts_altitude_Y_end.set_from_file(self.path+'/img/led-green.gif')
        self.fix.put(self.sts_altitude_Y_end, 705, 490)
        self.sts_altitude_Y_end.show()

        # ground: cur
        self.img_ground_cur = gtk.Image()
        self.img_ground_cur.set_from_file(self.path+'/img/gl_full_s.png')
        self.fix.put(self.img_ground_cur, 100, 500)
        self.img_ground_cur.show()
        # ground: cmd
        self.img_ground_cmd = gtk.Image()
        self.img_ground_cmd.set_from_file(self.path+'/img/al_empty_s.png')
        self.fix.put(self.img_ground_cmd, 100, 500)
        self.img_ground_cmd.show()
        
        # altitude: cur
        self.img_altitude_cur = gtk.Image()
        self.img_altitude_cur.set_from_file(self.path+'/img/al_full_s.png')
        self.fix.put(self.img_altitude_cur, 100, 450)
        self.img_altitude_cur.show()
        # altitude: cmd
        self.img_altitude_cmd = gtk.Image()
        self.img_altitude_cmd.set_from_file(self.path+'/img/al_empty_s.png')
        self.fix.put(self.img_altitude_cmd, 100, 450)
        self.img_altitude_cmd.show()
        ############ labels       ##########
        self.label1 = gtk.Label()
        self.label1.modify_font(pango.FontDescription("sans 8"))
        self.label1.set_text("Ground Layer")
        self.label1.show()
        self.fix.put(self.label1, 350, 680)

        self.label2 = gtk.Label()
        self.label2.modify_font(pango.FontDescription("sans 8"))
        self.label2.set_text("Altitude Layer X")
        self.label2.show()
        self.fix.put(self.label2, 350, 600)

        self.label3 = gtk.Label()
        self.label3.modify_font(pango.FontDescription("sans 8"))
        self.label3.set_angle(90)
        self.label3.set_text("Altitude Layer Y")
        self.label3.show()
        self.fix.put(self.label3, 690, 200)

        self.label4 = gtk.Label()
        self.label4.modify_font(pango.FontDescription("sans 8"))
        self.label4.set_text("Y: INIT POSITION")
        self.label4.show()
        self.fix.put(self.label4, 570, 470)
        
        self.label5 = gtk.Label()
        self.label5.modify_font(pango.FontDescription("sans 8"))
        self.label5.set_text("Y: END POSITION")
        self.label5.show()
        self.fix.put(self.label5, 570, 50)

        self.label6 = gtk.Label()
        self.label6.modify_font(pango.FontDescription("sans 8"))
        self.label6.set_text("X: INIT POSITION")
        self.label6.show()
        self.fix.put(self.label6, 5, 540)

        self.label7 = gtk.Label()
        self.label7.modify_font(pango.FontDescription("sans 8"))
        self.label7.set_text("X: END POSITION")
        self.label7.show()
        self.fix.put(self.label7, 570, 540)

        #ground x
        self.label8 = gtk.Label()
        self.label8.modify_font(pango.FontDescription("sans 8"))
        self.label8.set_text("position")
        self.label8.show()
        self.fix.put(self.label8, 75, 700)
        #
        self.label9 = gtk.Label()
        self.label9.modify_font(pango.FontDescription("sans 8"))
        self.label9.set_text("velocity")
        self.label9.show()
        self.fix.put(self.label9, 75, 715)
        #altitude x
        self.label10 = gtk.Label()
        self.label10.modify_font(pango.FontDescription("sans 8"))
        self.label10.set_text("position")
        self.label10.show()
        self.fix.put(self.label10, 75, 620)
        #
        self.label11 = gtk.Label()
        self.label11.modify_font(pango.FontDescription("sans 8"))
        self.label11.set_text("velocity")
        self.label11.show()
        self.fix.put(self.label11, 75, 635)

        #altitude y
        self.label12 = gtk.Label()
        self.label12.modify_font(pango.FontDescription("sans 8"))
        self.label12.set_angle(90)
        self.label12.set_text("position")
        self.label12.show()
        self.fix.put(self.label12, 705, 510)
        #
        self.label13 = gtk.Label()
        self.label13.modify_font(pango.FontDescription("sans 8"))
        self.label13.set_angle(90)
        self.label13.set_text("velocity")
        self.label13.show()
        self.fix.put(self.label13, 725, 510)
        ########################
        # ground_scale
        #
        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
        self.ground_scale_pos = gtk.HScale(adjustment)
        self.ground_scale_pos.set_digits(0)
        self.ground_scale_pos.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.ground_scale_pos.connect("value-changed", self.ground_scale_pos_moved)
        self.ground_scale_pos.set_size_request(500, 30)
        self.ground_scale_pos.show()
        self.fix.put(self.ground_scale_pos, 150, 680)
        ########################
        # ground_scale
        #
        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
        self.ground_scale_vel = gtk.HScale(adjustment)
        self.ground_scale_vel.set_digits(0)
        self.ground_scale_vel.set_update_policy(gtk.UPDATE_CONTINUOUS)
#        self.ground_scale_vel.connect("value-changed", self.ground_scale_vel_moved)
        self.ground_scale_vel.set_size_request(500, 30)
        self.ground_scale_vel.show()
        self.fix.put(self.ground_scale_vel, 150, 700)
        ########################
        # altitude_scale X
        #
        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
        self.altitude_scale_pos_X = gtk.HScale(adjustment)
        self.altitude_scale_pos_X.set_digits(0)
        self.altitude_scale_pos_X.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.altitude_scale_pos_X.connect("value-changed", self.altitude_scale_pos_X_moved)
        self.altitude_scale_pos_X.set_size_request(500, 30)
        self.altitude_scale_pos_X.show()
        self.fix.put(self.altitude_scale_pos_X, 150, 600)
        ########################
        # altitude_scale X
        #
        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
        self.altitude_scale_vel_X = gtk.HScale(adjustment)
        self.altitude_scale_vel_X.set_digits(0)
        self.altitude_scale_vel_X.set_update_policy(gtk.UPDATE_CONTINUOUS)
#        self.altitude_scale_vel_X.connect("value-changed", self.altitude_scale_vel_X_moved)
        self.altitude_scale_vel_X.set_size_request(500, 30)
        self.altitude_scale_vel_X.show()
        self.fix.put(self.altitude_scale_vel_X, 150, 622)
        ########################
        # altitude_scale Y
        #
        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
        self.altitude_scale_pos_Y = gtk.VScale(adjustment)
        self.altitude_scale_pos_Y.set_digits(0)
        #self.altitude_scale_pos_Y.set_value_pos(gtk.POS_BOTTOM) 
        self.altitude_scale_pos_Y.set_inverted(True)
        self.altitude_scale_pos_Y.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.altitude_scale_pos_Y.connect("value-changed", self.altitude_scale_pos_Y_moved)
        self.altitude_scale_pos_Y.set_size_request(30, 450)
        self.altitude_scale_pos_Y.show()
        self.fix.put(self.altitude_scale_pos_Y, 700, 40)
        ########################
        # altitude_scale Y
        #
        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
        self.altitude_scale_vel_Y = gtk.VScale(adjustment)
        self.altitude_scale_vel_Y.set_digits(0)
        #self.altitude_scale_vel_Y.set_value_pos(gtk.POS_BOTTOM) 
        self.altitude_scale_vel_Y.set_inverted(True)
        self.altitude_scale_vel_Y.set_update_policy(gtk.UPDATE_CONTINUOUS)
        #self.altitude_scale_vel_Y.connect("value-changed", self.altitude_scale_vel_Y_moved)
        self.altitude_scale_vel_Y.set_size_request(30, 450)
        self.altitude_scale_vel_Y.show()
        self.fix.put(self.altitude_scale_vel_Y, 720, 40)
        # Apply button:
        self.button_ok = gtk.Button("Execute Now")
        self.button_ok.show()
        self.fix.put(self.button_ok, 650, 750)

        ##Creating controller
        self.controller = Controller()

    def ground_scale_pos_moved(self, event):
        print "ground_scale_moved"
        print self.ground_scale_pos.get_value()
        self.fix.move(self.img_ground_cmd, 100+int(self.ground_scale_pos.get_value()*4), 500)

    def altitude_scale_pos_X_moved(self, event):
        print "altitude_scale_X_moved"
        print self.altitude_scale_pos_X.get_value()
        self.fix.move(self.img_altitude_cmd, 100+int(self.altitude_scale_pos_X.get_value()*4), 450 - int(self.altitude_scale_pos_Y.get_value()*4))

    def altitude_scale_pos_Y_moved(self, event):
        print "altitude_scale_Y_moved"
        print self.altitude_scale_pos_Y.get_value()
        self.fix.move(self.img_altitude_cmd, 100+int(self.altitude_scale_pos_X.get_value()*4), 450 - int(self.altitude_scale_pos_Y.get_value()*4))

if __name__ == '__main__':
    app = Layers()
    gtk.main()
