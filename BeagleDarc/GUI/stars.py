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
        self.win.set_size_request(800, 800)
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
        img.set_from_file('./img/star800.png')
        img.show()
        self.fix.put(img, 0, 0)
        ########################
        event_box = gtk.EventBox()
        self.win.add(event_box)
        event_box.show()

        #B1
        button = gtk.ToggleButton("1")
        button.connect("toggled", self.callback, "1")
        button.show()
        self.fix.put(button, 395 , 390)
        #B2
        button = gtk.ToggleButton("2")
        button.connect("toggled", self.callback, "2")
        button.show()
        self.fix.put(button, 385 , 420)
        #B3
        button = gtk.ToggleButton("3")
        button.connect("toggled", self.callback, "3")
        button.show()
        self.fix.put(button, 372 , 383)
        #B4
        button = gtk.ToggleButton("4")
        button.connect("toggled", self.callback, "4")
        button.show()
        self.fix.put(button, 401 , 364)
        #B5
        button = gtk.ToggleButton("5")
        button.connect("toggled", self.callback, "5")
        button.show()
        self.fix.put(button, 423 , 397)

        button = gtk.ToggleButton("6")
        button.connect("toggled", self.callback, "6")
        button.show()
        self.fix.put(button, 386 , 469)

        button = gtk.ToggleButton("7")
        button.connect("toggled", self.callback, "7")
        button.show()
        self.fix.put(button, 334 , 440)

        button = gtk.ToggleButton("8")
        button.connect("toggled", self.callback, "8")
        button.show()
        self.fix.put(button, 320 , 384)

        button = gtk.ToggleButton("9")
        button.connect("toggled", self.callback, "9")
        button.show()
        self.fix.put(button, 342 , 332)

        button = gtk.ToggleButton("10")
        button.connect("toggled", self.callback, "10")
        button.show()
        self.fix.put(button, 394 , 312)

        button = gtk.ToggleButton("11")
        button.connect("toggled", self.callback, "11")
        button.show()
        self.fix.put(button, 457 , 338)

        button = gtk.ToggleButton("12")
        button.connect("toggled", self.callback, "12")
        button.show()
        self.fix.put(button, 470 , 395)

        button = gtk.ToggleButton("13")
        button.connect("toggled", self.callback, "13")
        button.show()
        self.fix.put(button, 442 , 455)

        button = gtk.ToggleButton("14")
        button.connect("toggled", self.callback, "14")
        button.show()
        self.fix.put(button, 385 , 520)

        button = gtk.ToggleButton("15")
        button.connect("toggled", self.callback, "15")
        button.show()
        self.fix.put(button, 298 , 476)

        button = gtk.ToggleButton("16")
        button.connect("toggled", self.callback, "16")
        button.show()
        self.fix.put(button, 270 , 385)

        button = gtk.ToggleButton("17")
        button.connect("toggled", self.callback, "17")
        button.show()
        self.fix.put(button, 311 , 296)

        button = gtk.ToggleButton("18")
        button.connect("toggled", self.callback, "18")
        button.show()
        self.fix.put(button, 390 , 260)

        button = gtk.ToggleButton("19")
        button.connect("toggled", self.callback, "19")
        button.show()
        self.fix.put(button, 490 , 300)

        button = gtk.ToggleButton("20")
        button.connect("toggled", self.callback, "20")
        button.show()
        self.fix.put(button, 525 , 401)

        button = gtk.ToggleButton("21")
        button.connect("toggled", self.callback, "21")
        button.show()
        self.fix.put(button, 480 , 490)

        button = gtk.ToggleButton("22")
        button.connect("toggled", self.callback, "22")
        button.show()
        self.fix.put(button, 385 , 565)

        button = gtk.ToggleButton("23")
        button.connect("toggled", self.callback, "23")
        button.show()
        self.fix.put(button, 319 , 556)

        button = gtk.ToggleButton("24")
        button.connect("toggled", self.callback, "24")
        button.show()
        self.fix.put(button, 263 , 515)

        button = gtk.ToggleButton("25")
        button.connect("toggled", self.callback, "25")
        button.show()
        self.fix.put(button, 220 , 450)

        button = gtk.ToggleButton("26")
        button.connect("toggled", self.callback, "26")
        button.show()
        self.fix.put(button, 215 , 383)

        button = gtk.ToggleButton("27")
        button.connect("toggled", self.callback, "27")
        button.show()
        self.fix.put(button, 230 , 314)

        button = gtk.ToggleButton("28")
        button.connect("toggled", self.callback, "28")
        button.show()
        self.fix.put(button, 275 , 260)

        button = gtk.ToggleButton("29")
        button.connect("toggled", self.callback, "29")
        button.show()
        self.fix.put(button, 330 , 222)

        button = gtk.ToggleButton("30")
        button.connect("toggled", self.callback, "30")
        button.show()
        self.fix.put(button, 390 , 210)

        button = gtk.ToggleButton("31")
        button.connect("toggled", self.callback, "31")
        button.show()
        self.fix.put(button, 470 , 225)

        button = gtk.ToggleButton("32")
        button.connect("toggled", self.callback, "32")
        button.show()
        self.fix.put(button, 525 , 265)

        button = gtk.ToggleButton("33")
        button.connect("toggled", self.callback, "33")
        button.show()
        self.fix.put(button, 566 , 332)

        button = gtk.ToggleButton("34")
        button.connect("toggled", self.callback, "34")
        button.show()
        self.fix.put(button, 575 , 395)

        button = gtk.ToggleButton("35")
        button.connect("toggled", self.callback, "35")
        button.show()
        self.fix.put(button, 555 , 467)

        button = gtk.ToggleButton("36")
        button.connect("toggled", self.callback, "36")
        button.show()
        self.fix.put(button, 510 , 527)

        button = gtk.ToggleButton("37")
        button.connect("toggled", self.callback, "37")
        button.show()
        self.fix.put(button, 450 , 560)

        button = gtk.ToggleButton("38")
        button.connect("toggled", self.callback, "38")
        button.show()
        self.fix.put(button, 425 , 620)

        button = gtk.ToggleButton("39")
        button.connect("toggled", self.callback, "39")
        button.show()
        self.fix.put(button, 335 , 615)

        button = gtk.ToggleButton("40")
        button.connect("toggled", self.callback, "40")
        button.show()
        self.fix.put(button, 259 , 582)

        button = gtk.ToggleButton("41")
        button.connect("toggled", self.callback, "41")
        button.show()
        self.fix.put(button, 195 , 510)

        button = gtk.ToggleButton("42")
        button.connect("toggled", self.callback, "42")
        button.show()
        self.fix.put(button, 167 , 427)

        button = gtk.ToggleButton("43")
        button.connect("toggled", self.callback, "43")
        button.show()
        self.fix.put(button, 170 , 338)

        button = gtk.ToggleButton("44")
        button.connect("toggled", self.callback, "44")
        button.show()
        self.fix.put(button, 209 , 254)

        button = gtk.ToggleButton("45")
        button.connect("toggled", self.callback, "45")
        button.show()
        self.fix.put(button, 271 , 195)

        button = gtk.ToggleButton("46")
        button.connect("toggled", self.callback, "46")
        button.show()
        self.fix.put(button, 355 , 160)

        button = gtk.ToggleButton("47")
        button.connect("toggled", self.callback, "47")
        button.show()
        self.fix.put(button, 445 , 165)

        button = gtk.ToggleButton("48")
        button.connect("toggled", self.callback, "48")
        button.show()
        self.fix.put(button, 525 , 195)

        button = gtk.ToggleButton("49")
        button.connect("toggled", self.callback, "49")
        button.show()
        self.fix.put(button, 590 , 265)

        button = gtk.ToggleButton("50")
        button.connect("toggled", self.callback, "50")
        button.show()
        self.fix.put(button, 620 , 350)

        button = gtk.ToggleButton("51")
        button.connect("toggled", self.callback, "51")
        button.show()
        self.fix.put(button, 621 , 444)

        button = gtk.ToggleButton("52")
        button.connect("toggled", self.callback, "52")
        button.show()
        self.fix.put(button, 580 , 527)

        button = gtk.ToggleButton("53")
        button.connect("toggled", self.callback, "53")
        button.show()
        self.fix.put(button, 510 , 587)

        button = gtk.ToggleButton("54")
        button.connect("toggled", self.callback, "54")
        button.show()
        self.fix.put(button, 380 , 670)

        button = gtk.ToggleButton("55")
        button.connect("toggled", self.callback, "55")
        button.show()
        self.fix.put(button, 279 , 651)

        button = gtk.ToggleButton("56")
        button.connect("toggled", self.callback, "56")
        button.show()
        self.fix.put(button, 185 , 584)

        button = gtk.ToggleButton("57")
        button.connect("toggled", self.callback, "57")
        button.show()
        self.fix.put(button, 130 , 493)

        button = gtk.ToggleButton("58")
        button.connect("toggled", self.callback, "58")
        button.show()
        self.fix.put(button, 110 , 385)

        button = gtk.ToggleButton("59")
        button.connect("toggled", self.callback, "59")
        button.show()
        self.fix.put(button, 138 , 273)

        button = gtk.ToggleButton("60")
        button.connect("toggled", self.callback, "60")
        button.show()
        self.fix.put(button, 201 , 184)

        button = gtk.ToggleButton("61")
        button.connect("toggled", self.callback, "61")
        button.show()
        self.fix.put(button, 289 , 123)

        button = gtk.ToggleButton("62")
        button.connect("toggled", self.callback, "62")
        button.show()
        self.fix.put(button, 395 , 110)

        button = gtk.ToggleButton("63")
        button.connect("toggled", self.callback, "63")
        button.show()
        self.fix.put(button, 504 , 128)

        button = gtk.ToggleButton("64")
        button.connect("toggled", self.callback, "64")
        button.show()
        self.fix.put(button, 595 , 200)

        button = gtk.ToggleButton("65")
        button.connect("toggled", self.callback, "65")
        button.show()
        self.fix.put(button, 655 , 290)

        button = gtk.ToggleButton("66")
        button.connect("toggled", self.callback, "66")
        button.show()
        self.fix.put(button, 670 , 400)

        button = gtk.ToggleButton("67")
        button.connect("toggled", self.callback, "67")
        button.show()
        self.fix.put(button, 650 , 505)

        button = gtk.ToggleButton("68")
        button.connect("toggled", self.callback, "68")
        button.show()
        self.fix.put(button, 585 , 595)

        button = gtk.ToggleButton("69")
        button.connect("toggled", self.callback, "69")
        button.show()
        self.fix.put(button, 490 , 655)

        button = gtk.ToggleButton("70")
        button.connect("toggled", self.callback, "70")
        button.show()
        self.fix.put(button, 386 , 724)

        button = gtk.ToggleButton("71")
        button.connect("toggled", self.callback, "71")
        button.show()
        self.fix.put(button, 317 , 713)

        button = gtk.ToggleButton("72")
        button.connect("toggled", self.callback, "72")
        button.show()
        self.fix.put(button, 255 , 696)

        button = gtk.ToggleButton("73")
        button.connect("toggled", self.callback, "73")
        button.show()
        self.fix.put(button, 200 , 662)

        button = gtk.ToggleButton("74")
        button.connect("toggled", self.callback, "74")
        button.show()
        self.fix.put(button, 153 , 620)

        button = gtk.ToggleButton("75")
        button.connect("toggled", self.callback, "75")
        button.show()
        self.fix.put(button, 112 , 568)

        button = gtk.ToggleButton("76")
        button.connect("toggled", self.callback, "76")
        button.show()
        self.fix.put(button, 83 , 508)

        button = gtk.ToggleButton("77")
        button.connect("toggled", self.callback, "77")
        button.show()
        self.fix.put(button, 64 , 448)

        button = gtk.ToggleButton("78")
        button.connect("toggled", self.callback, "78")
        button.show()
        self.fix.put(button, 60 , 382)

        button = gtk.ToggleButton("79")
        button.connect("toggled", self.callback, "79")
        button.show()
        self.fix.put(button, 71 , 318)

        button = gtk.ToggleButton("80")
        button.connect("toggled", self.callback, "80")
        button.show()
        self.fix.put(button, 90 , 254)

        button = gtk.ToggleButton("81")
        button.connect("toggled", self.callback, "81")
        button.show()
        self.fix.put(button, 121 , 195)

        button = gtk.ToggleButton("82")
        button.connect("toggled", self.callback, "82")
        button.show()
        self.fix.put(button, 162 , 150)

        button = gtk.ToggleButton("83")
        button.connect("toggled", self.callback, "83")
        button.show()
        self.fix.put(button, 215 , 111)

        button = gtk.ToggleButton("84")
        button.connect("toggled", self.callback, "84")
        button.show()
        self.fix.put(button, 271 , 82)

        button = gtk.ToggleButton("85")
        button.connect("toggled", self.callback, "85")
        button.show()
        self.fix.put(button, 335 , 67)

        button = gtk.ToggleButton("86")
        button.connect("toggled", self.callback, "86")
        button.show()
        self.fix.put(button, 395 , 55)

        button = gtk.ToggleButton("87")
        button.connect("toggled", self.callback, "87")
        button.show()
        self.fix.put(button, 465 , 65)

        button = gtk.ToggleButton("88")
        button.connect("toggled", self.callback, "88")
        button.show()
        self.fix.put(button, 525 , 85)

        button = gtk.ToggleButton("89")
        button.connect("toggled", self.callback, "89")
        button.show()
        self.fix.put(button, 582 , 115)

        button = gtk.ToggleButton("90")
        button.connect("toggled", self.callback, "90")
        button.show()
        self.fix.put(button, 630 , 157)

        button = gtk.ToggleButton("91")
        button.connect("toggled", self.callback, "91")
        button.show()
        self.fix.put(button, 675 , 210)

        button = gtk.ToggleButton("92")
        button.connect("toggled", self.callback, "92")
        button.show()
        self.fix.put(button, 700 , 270)

        button = gtk.ToggleButton("93")
        button.connect("toggled", self.callback, "93")
        button.show()
        self.fix.put(button, 720 , 335)

        button = gtk.ToggleButton("94")
        button.connect("toggled", self.callback, "94")
        button.show()
        self.fix.put(button, 725 , 395)

        button = gtk.ToggleButton("95")
        button.connect("toggled", self.callback, "95")
        button.show()
        self.fix.put(button, 715 , 465)

        button = gtk.ToggleButton("96")
        button.connect("toggled", self.callback, "96")
        button.show()
        self.fix.put(button, 695 , 525)

        button = gtk.ToggleButton("97")
        button.connect("toggled", self.callback, "97")
        button.show()
        self.fix.put(button, 663 , 580)

        button = gtk.ToggleButton("98")
        button.connect("toggled", self.callback, "98")
        button.show()
        self.fix.put(button, 620 , 634)

        button = gtk.ToggleButton("99")
        button.connect("toggled", self.callback, "99")
        button.show()
        self.fix.put(button, 570 , 677)

        button = gtk.ToggleButton("100")
        button.connect("toggled", self.callback, "100")
        button.show()
        self.fix.put(button, 508 , 705)

        button = gtk.ToggleButton("101")
        button.connect("toggled", self.callback, "101")
        button.show()
        self.fix.put(button, 445 , 721)

    def callback(self, widget, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        #print widget.get_active()
        
    def show_flower(self, widget, event):
        count = 0
        if event.type == gtk.gdk.BUTTON_PRESS:
            count = 1
        elif event.type == gtk.gdk._2BUTTON_PRESS:
            count = 2
        elif event.type == gtk.gdk._3BUTTON_PRESS:
            count = 3

        for i in range(count):
            img = gtk.Image()
            #img.set_from_file('./face-kiss.png')
            #img.show()
            x = int(event.x) + (i*self.img_size)
            y = int(event.y) 
            coord = """
            button = gtk.ToggleButton("2")
            button.connect("toggled", self.callback, "2")
            button.show()
            self.fix.put(button, %d , %d)""" % (x,y)
            #self.fix.put(img, x, y)
            print coord
            self.label = gtk.Label('X')
            self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
            self.label.show()
            self.fix.put(self.label, x, y)

if __name__ == '__main__':
    app = Main()
    gtk.main()
