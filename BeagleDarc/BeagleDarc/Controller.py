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
        pass
    #star methods
    def star_on(self, star):
        pass
    def star_off(self, star):
        pass

    #layer methods
    def layer_move(self, layer):
        pass

    def layer_move_skip_sensor(self, layer):
        pass

if __name__ == '__main__':
    c = Controller()

