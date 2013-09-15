#!/usr/bin/python 
'''
Controller
'''

from BeagleDarc.Model import Star

class Controller:
    '''
    Controller:
    '''
    def __init__(self):
        '''
        '''
        pass

    def turn_on(self, star):
        l = Star(star)
        l.set_on()

    def turn_off(self, star):
        l = Star(star)
        l.set_off()

if __name__ == '__main__':
    c = Controller()
    c.turn_on(1)
