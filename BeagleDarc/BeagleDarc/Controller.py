#!/usr/bin/python 
'''
Controller
'''

from BeagleDarc.Peripherals  import Led
from BeagleDarc.Model import Model
class Controller:
    '''
    Controller:
    '''
    def __init__(self):
        '''
        '''
        self.Led = Led
        self.model = Model()

    def turn_on(self, star):
        l = self.Led(star)
        config_name = "led_%d" % star
        self.model.get_star_name(config_name)
        l.set_on()

if __name__ == '__main__':
    c = Controller()
    c.turn_on(1)
