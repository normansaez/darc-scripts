import sys
import pygtk  
pygtk.require("2.0")  
import gtk  

from BeagleDarc.Model import Model

class BeagleDarcGui:

    wTree = gtk.Builder()

    def __init__( self ):
        self.model = Model()
        serverhost = self.model.get_beagledarc_server_host()
        serveruser = self.model.get_beagledarc_server_user()
        serverpasswd = self.model.get_beagledarc_server_password()
        serverport = self.model.get_beagledarc_server_port()

        self.builder = gtk.Builder()
        self.builder.add_from_file("glade/beagledarc.glade")
        self.window = self.builder.get_object ("window1")
#        self.window.set_icon_from_file('img/icon-beagle.png')

        if self.window:
            self.window.connect("destroy", gtk.main_quit)

        self.entry1 = self.builder.get_object ("entry1")
        self.entry2 = self.builder.get_object ("entry2")
        self.entry3 = self.builder.get_object ("entry3")
        self.entry4 = self.builder.get_object ("entry4")

        self.entry1.set_text(serverhost) 
        self.entry2.set_text(serveruser) 
        self.entry3.set_text(serverpasswd) 
        self.entry4.set_text(serverport) 

        dic = { 
            "on_buttonQuit_clicked" : self.quit,
            "on_window1_destroy" : self.quit,
            "gtk_widget_destroy" : self.quit,
            "on_phasescreen_menuitem_activate" : self.phasescreen,
            "on_stars_menuitem_activate" : self.stars,
            "connect_button_released_cb": self.connect
        }
        
        self.builder.connect_signals( dic )

    def quit(self, widget):
        sys.exit(0)

    def connect(self, widget):
        print "connected :)"

    def phasescreen(self, widget):
        print "phasescreen"

    def stars(self, widget):
        from GUI import Stars
        Stars.Main()

BeagleDarcGui = BeagleDarcGui()
BeagleDarcGui.window.show()
gtk.main()
