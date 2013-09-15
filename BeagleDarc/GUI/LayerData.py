#!/usr/bin/env python
import os
import sys
import pygtk  
pygtk.require("2.0")  
import gtk  
import gobject

from subprocess import Popen, PIPE
from BeagleDarc.Model import Layer

class LayerData:

    wTree = gtk.Builder()

    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))
        self.builder = gtk.Builder()
        self.builder.add_from_file(path+"/glade/layer_data.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.window.show()

        if self.window:
            self.window.connect("destroy", gtk.main_quit)

        ## star combo
        store = gtk.ListStore(gobject.TYPE_STRING)
        store.append(["vertical_altitude_layer"])
        store.append(["horizontal_altitude_layer"])
        store.append(["ground_layer"])

        self.combobox_layer = self.builder.get_object("combobox_layer")
        self.combobox_layer.connect('changed', self.changed_cb)
        self.combobox_layer.set_model(store)

        cell = gtk.CellRendererText()
        self.combobox_layer.pack_start(cell, True)
        self.combobox_layer.add_attribute(cell, 'text', 0)
    
        #PIN
        self.entry_pin_enable = self.builder.get_object("entry_pin_enable")
        #PIN
        self.entry_pin_steps = self.builder.get_object("entry_pin_steps")
        #PIN
        self.entry_pin_direction = self.builder.get_object("entry_pin_direction")
        
        #NAME
        self.entry_name = self.builder.get_object("entry_name")
        #SIM
        self.checkbutton_sim = self.builder.get_object("checkbutton_sim")
        
        #DIRECTION
        store_exp = gtk.ListStore(gobject.TYPE_STRING)
        store_exp.append(["INIT_POSITION"])
        store_exp.append(["END_POSITION"])
        self.combobox_direction = self.builder.get_object("combobox_direction")
        self.combobox_direction.set_model(store_exp)
        cell_exp = gtk.CellRendererText()
        self.combobox_direction.pack_start(cell_exp, True)
        self.combobox_direction.add_attribute(cell_exp, 'text', 0)

#        #VELOCITY
#        self.hscale_vel = self.builder.get_object("hscale_vel")
#        adjustment = gtk.Adjustment(value=0.0, lower=0.0, upper=101.0, step_incr=0.1, page_incr=1.0, page_size=1.0)
#        self.hscale_vel.set_adjustment(adjustment)
#        self.hscale_vel.set_digits(0)
#        #self.hscale_vel.set_update_policy(gtk.UPDATE_CONTINUOUS)
#        self.hscale_vel.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
#        #self.hscale_vel.set_update_policy(gtk.UPDATE_DELAYED)
#        self.hscale_vel.connect("value-changed", self.velocity)
#
        #STEPS
        self.entry_steps = self.builder.get_object("entry_steps")
        
        #VR_INIT
        self.entry_vr_init = self.builder.get_object("entry_vr_init")

        #VR_END
        self.entry_vr_end = self.builder.get_object("entry_vr_end")

        #VR_END
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

    def fill_info(self, config_name):
        layer = Layer(config_name)
        self.entry_pin_enable.set_text(layer.pin_enable)
        self.entry_pin_steps.set_text(layer.pin_steps)
        self.entry_pin_direction.set_text(layer.pin_direction)
        self.entry_name.set_text(layer.name)
        if layer.simulated is True:
            self.checkbutton_sim.set_active(layer.simulated)
        self.combobox_direction.insert_text(0, str(layer.direction)) 
        self.combobox_direction.set_active(0)
        #self.hscale_vel.set_value(int(self.model.get_motor_velocity(config_name)))
        self.entry_steps.set_text(str(layer.steps))
        self.entry_vr_init.set_text(str(layer.vr_init))
        self.entry_vr_end.set_text(str(layer.vr_end))
        self.entry_image_prefix.set_text(layer.image_prefix)

    def changed_cb(self, entry):
        layer = self.combobox_layer.get_active_text()
        print 'Getting layer: ', layer
        self.fill_info(layer)
        return

    def velocity(self, event):
        #print self.hscale_vel.get_value()
        pass

    def save(self, widget):
        print "### SAVE ###"
        config_name = self.combobox_layer.get_active_text() 
        layer = Layer(config_name)
        layer.pin_enable = self.entry_pin_enable.get_text()
        layer.pin_steps = self.entry_pin_steps.get_text()
        layer.pin_direction = self.entry_pin_direction.get_text()
        layer.name = self.entry_name.get_text()
        layer.sim = self.checkbutton_sim.get_active()
        layer.direction = self.combobox_direction.get_active_text()
        #layer.velocity = int(self.hscale_vel.get_value())
        layer.steps = self.entry_steps.get_text()
        layer.vr_init = self.entry_vr_init.get_text()
        layer.vr_end = self.entry_vr_end.get_text()
        layer.image_prefix = self.entry_image_prefix.get_text()
        print layer.pin_enable
        print layer.pin_steps
        print layer.pin_direction
        print layer.name 
        print layer.sim
        print layer.direction
        print layer.velocity
        print layer.steps
        print layer.vr_init
        print layer.vr_end
        print layer.image_prefix
        print "### SAVE ###"

    def default(self, widget):
        print "default"
        layer = self.combobox_layer.get_active_text() 
        print "getting info from layer: %s" % layer
        self.fill_info(layer)
        print "restored"

    def quit(self, widget):
        print "bla"

if __name__ == '__main__':
    LayerData = LayerData()
    gtk.main()
