#!/usr/bin/env python
import os
import sys
import pygtk  
pygtk.require("2.0")  
import gtk  
import gobject

from subprocess import Popen, PIPE
from BeagleDarc.Model import Star


class StarData:

    wTree = gtk.Builder()

    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))

        self.builder = gtk.Builder()
        self.builder.add_from_file(path+"/glade/star_data.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.window.show()

        if self.window:
            self.window.connect("destroy", gtk.main_quit)

        ## star combo
        store = gtk.ListStore(gobject.TYPE_STRING)
        for i in range(1,100):
            store.append([str(i)])

        self.combobox_star = self.builder.get_object("combobox_star")
        self.combobox_star.connect('changed', self.changed_cb)
        self.combobox_star.set_model(store)

        #Necesary for combobox but no for comboboxentry
        cell = gtk.CellRendererText()
        self.combobox_star.pack_start(cell, True)
        self.combobox_star.add_attribute(cell, 'text', 0)
    
        #PIN
        self.entry_pin_led = self.builder.get_object("entry_pin_led")
        #PIN
        self.entry_pin_group = self.builder.get_object("entry_pin_group")
        #PIN
        self.entry_pin_enable = self.builder.get_object("entry_pin_enable")
        
        #NAME
        self.entry_name = self.builder.get_object("entry_name")
        #SIM
        self.checkbutton_sim = self.builder.get_object("checkbutton_sim")
        
        #EXP_T
        store_exp = gtk.ListStore(gobject.TYPE_STRING)
        #mili seconds (0 to 1 min)
        for i in range(0,60000,1000):
            store_exp.append([str(i)])
        self.combobox_exp_time = self.builder.get_object("combobox_exp_time")
        self.combobox_exp_time.set_model(store_exp)
        self.combobox_exp_time.set_text_column(0)
        
        #BRIGHT
        store_bright = gtk.ListStore(gobject.TYPE_STRING)
        for i in range(0,100):
            store_bright.append([str(i)])
        self.combobox_brightness = self.builder.get_object("combobox_brightness")
        self.combobox_brightness.set_model(store_bright)
        cell = gtk.CellRendererText()
        self.combobox_brightness.pack_start(cell, True)
        self.combobox_brightness.add_attribute(cell, 'text', 0)
        
        #IMG_PRE
        self.entry_image_prefix = self.builder.get_object("entry_image_prefix")

        #SAVE/RESTORE BUTTONS
        self.button_default = self.builder.get_object("button_default")
        self.button_save = self.builder.get_object("button_save")

        dic = { 
            "on_window1_destroy" : self.quit,
            "on_button_save_clicked" : self.save,
            'on_button_default_clicked'  : self.default
        }
        self.builder.connect_signals(dic)

    def fill_info(self, star_id):
        star = Star(int(star_id))
        self.entry_pin_led.set_text(star.pin_led)
        self.entry_pin_group.set_text(star.pin_group)
        self.entry_pin_enable.set_text(star.pin_enable)
        self.entry_name.set_text(star.name)
        if star.simulated is True:
            self.checkbutton_sim.set_active(star.simulated)
        self.combobox_exp_time.insert_text(0, str(star.exp_time)) 
        self.combobox_exp_time.set_active(0)
        self.combobox_brightness.insert_text(0, str(star.brightness)) 
        self.combobox_brightness.set_active(0)
        self.entry_image_prefix.set_text(star.image_prefix)

    def changed_cb(self, entry):
        star = int(entry.get_active_text())
        print 'Getting star: ', star
        self.fill_info(star)
        return

    def quit(self, widget):
        sys.exit(0)

    def save(self, widget):
        star = Star(int(self.combobox_star.get_active_text()))
        star.pin_led = self.entry_pin_led.get_text()
        star.pin_group = self.entry_pin_group.get_text()
        star.pin_enable = self.entry_pin_enable.get_text()
        star.name = self.entry_name.get_text()
        star.sim = self.checkbutton_sim.get_active()
        star.exp_time = self.combobox_exp_time.get_active_text()
        star.bright = self.combobox_brightness.get_active_text()
        star.img_prefix = self.entry_image_prefix.get_text()
        print star.pin_led
        print star.pin_group
        print star.pin_enable
        print star.name 
        print star.sim
        print star.exp_time
        print star.bright
        print star.img_prefix
        print "------------"
        print "saved"

    def default(self, widget):
        star = self.combobox_star.get_active_text() 
        print "getting info from star: %s" % star
        self.fill_info(star)
        print "restored"


if __name__ == '__main__':
    StarData = StarData()
    gtk.main()
