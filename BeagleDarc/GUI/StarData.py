#!/usr/bin/env python
import os
import sys
import pygtk  
pygtk.require("2.0")  
import gtk  
import gobject

from subprocess import Popen, PIPE
from BeagleDarc.Model import Model

class StarData:

    wTree = gtk.Builder()

    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))
        self.model = Model()

        self.builder = gtk.Builder()
        self.builder.add_from_file(path+"/glade/star_data.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.window.show()

        #if self.window:
        #    self.window.connect("destroy", gtk.main_quit)

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
        self.entry_pin = self.builder.get_object("entry_pin")
        
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

    def fill_info(self, star):
        try:
            config_name = 'led_%s' % star
            self.entry_pin.set_text(self.model.get_star_pin(config_name))
            self.entry_name.set_text(self.model.get_star_name(config_name))
            simulated  = self.model.get_star_simulated(config_name)
            if simulated is True:
                self.checkbutton_sim.set_active(True)
            self.combobox_exp_time.insert_text(0, str(self.model.get_star_exp_time(config_name))) 
            self.combobox_exp_time.set_active(0)
            self.combobox_brightness.insert_text(0, str(self.model.get_star_brightness(config_name))) 
            self.combobox_brightness.set_active(0)
            self.entry_image_prefix.set_text(self.model.get_star_image_prefix(config_name))
        except Exception, e:
            print e
            #print "no section configured"

    def changed_cb(self, entry):
        star = entry.get_active_text()
        print 'Getting star: ', star
        self.fill_info(star)
        return

    def quit(self, widget):
        sys.exit(0)

    def save(self, widget):
        star = self.combobox_star.get_active_text() 
        #try:
        config_name = 'led_%s' % star
        pin = self.entry_pin.get_text()
        name = self.entry_name.get_text()
        sim = self.checkbutton_sim.get_active()
        exp_time = self.combobox_exp_time.get_active_text()
        bright = self.combobox_brightness.get_active_text()
        img_prefix = self.entry_image_prefix.get_text()
        #set
        self.model.set_star_pin(config_name, value=pin)
        self.model.set_star_name(config_name, value=name)
        self.model.set_star_simulated(config_name, value=sim)
        self.model.set_star_exp_time(config_name, value=exp_time)
        self.model.set_star_brightness(config_name, value=bright)
        self.model.set_star_image_prefix(config_name, value=img_prefix)
        print pin
        print name 
        print sim
        print exp_time
        print bright
        print img_prefix
        print "------------"
        print "saved"
        #except Exception, e:
        #    print e

    def default(self, widget):
        star = self.combobox_star.get_active_text() 
        print "getting info from star: %s" % star
        self.fill_info(star)
        print "restored"


if __name__ == '__main__':
    StarData = StarData()
    gtk.main()
