#!/usr/bin/python 
'''
Controller
'''

from BeagleDarc.BeagleDarcClient import BeagleDarcClient
from BeagleDarc.Model import Star
from BeagleDarc.Model import Layer

class Controller:
    '''
    Controller:
    '''
    def __init__(self):
        '''
        '''
        #check server, partirlo remoto o local.
        pass
    #star methods
    def star_on(self, star_id):
        star = Star(star_id)
        pass
    def star_off(self, star_id):
        star = Star(star_id)
        pass

    #layer methods
    def layer_move(self, layer_id):
        layer = Layer(layer_id)
        pass
    def layer_move_skip_sensor(self, layer_id):
        layer = Layer(layer_id)
        pass

if __name__ == '__main__':
    c = Controller()
    c.star_on(1)
    c.star_off(1)
    c.layer_move('ground_layer')
    c.layer_move_skip_sensor('ground_layer')
