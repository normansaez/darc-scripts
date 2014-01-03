#!/usr/bin/python 
'''
Controller
'''

from BeagleDarc.BeagleDarcClient import BeagleDarcClient
from BeagleDarc.Model import BeagleDarcServerM 
from BeagleDarc.Model import Star
from BeagleDarc.Model import Layer

import CORBA, BBBServer

class Controller:
    '''
    Controller:
    '''
    def __init__(self):
        '''
        '''
        orb = CORBA.ORB_init()
        bds = BeagleDarcServerM('beagledarc_server')

        self.cli_obj = orb.string_to_object(bds.ior)

    #star methods
    def star_on(self, star_id):
        star = Star(star_id)
        #self.cli_obj.led_on(star.name, star.pin_led, star.pin_pwm, star.pin_enable)
        self.cli_obj.led_on(star.name, star.pin_led, star.pin_group, star.pin_enable)


    def star_off(self, star_id):
        star = Star(star_id)
#        self.cli_obj.led_off(name, pin_led, pin_pwm, pin_enable)

    #layer methods
    def layer_move(self, layer_id):
        layer = Layer(layer_id)
#        self.cli_obj.motor_move(name, steps, vel, pin_dir, pin_step, pin_sleep, stat_der, stat_izq)

    def layer_move_skip_sensor(self, layer_id):
        layer = Layer(layer_id)

if __name__ == '__main__':
    c = Controller()
    c.star_on(1)
    c.star_off(1)
    c.layer_move('ground_layer')
    c.layer_move_skip_sensor('ground_layer')
