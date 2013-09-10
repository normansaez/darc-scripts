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

        if self.window:
            self.window.connect("destroy", gtk.main_quit)

        ## star combo
        store = gtk.ListStore(gobject.TYPE_STRING)
        #store = gtk.ListStore(str)
        for i in range(1,100):
            store.append([str(i)])

        self.combobox_star = self.builder.get_object("combobox_star")
        self.combobox_star.child.connect('changed', self.changed_cb)
        self.combobox_star.set_model(store)
        self.combobox_star.set_text_column(0)
        #self.combobox_star.set_active(0)

        #this could be added , but it seems unnecesary
        #cell = gtk.CellRendererText()
        #self.combobox_star.pack_start(cell, True)
        #self.combobox_star.add_attribute(cell, 'text', 0)

    def changed_cb(self, entry):
        print 'Getting star: ', entry.get_text()
        return

    def quit(self, widget):
        sys.exit(0)


if __name__ == '__main__':
    StarData = StarData()
    StarData.window.show()
    gtk.main()
