
import os
import sys
import pygtk  
pygtk.require("2.0")  
import gtk  

from subprocess import Popen, PIPE

from BeagleDarc.Model import Model

class BeagleDarcGui:

    wTree = gtk.Builder()

    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))
        self.model = Model()
        self.serverhost = self.model.get_beagledarc_server_host()
        self.serveruser = self.model.get_beagledarc_server_user()
        self.serverpasswd = self.model.get_beagledarc_server_password()
        self.serverport = self.model.get_beagledarc_server_port()

        self.builder = gtk.Builder()
        self.builder.add_from_file(path+"/glade/beagledarc.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events() | gtk.gdk.BUTTON_PRESS_MASK)

        if self.window:
            self.window.connect("destroy", gtk.main_quit)

        #Toggle button to connect to beaglebone
        self.connect_togglebutton = self.builder.get_object ("connect_togglebutton")
        self.connect_togglebutton.connect("toggled", self.callback, "Connection")

        #default entries
        self.entry1 = self.builder.get_object ("entry1")
        self.entry2 = self.builder.get_object ("entry2")
        self.entry3 = self.builder.get_object ("entry3")
        self.entry4 = self.builder.get_object ("entry4")

        self.entry1.set_text(self.serverhost) 
        self.entry2.set_text(self.serveruser) 
        self.entry3.set_text(self.serverpasswd) 
        self.entry4.set_text(self.serverport) 

        dic = { 
            "on_buttonQuit_clicked" : self.quit,
            "on_window1_destroy" : self.quit,
            "gtk_widget_destroy" : self.quit,
            "on_phasescreen_menuitem_activate" : self.phasescreen,
            "on_stars_menuitem_activate" : self.stars
        }
        
        self.builder.connect_signals( dic )

    def callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        if widget.get_active() is True:
            cmd = "ssh %s@%s \"python /home/root/server.py &\"" % (self.serveruser, self.serverhost)
        if widget.get_active() is False:
            cmd = "ssh %s@%s \"ps aux |grep server.py|awk \'{print \\$2}\'|xargs kill -9\"" % (self.serveruser, self.serverhost)
        #process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
        process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
        sts = process.wait()
        #out = process.stdout.read().strip()
        #err = process.stderr.read().strip()
        #print cmd

    def quit(self, widget):
        sys.exit(0)


    def phasescreen(self, widget):
        print "phasescreen"

    def stars(self, widget):
        from GUI import Stars
        Stars.Main()

BeagleDarcGui = BeagleDarcGui()
BeagleDarcGui.window.show()
gtk.main()
