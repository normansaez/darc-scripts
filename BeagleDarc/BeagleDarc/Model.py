#!/usr/bin/python 
'''
Model
Handle file configurations between GUI/Controller
'''
import sys
import os
import time
import glob
import logging
import ConfigParser

class BD:
    def __init__(self):
        path, fil = os.path.split(os.path.abspath(__file__))
        self.configfile=path+'/configurations.cfg'
        self.config = None
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configfile)

    def write(self, config_name, property_name, value):
        cfgfile = open(self.configfile,'w')
        self.config.set(config_name, str(property_name), str(value))
        self.config.write(cfgfile)
        cfgfile.close()

class Layer(object):
    def __init__(self, config_name):
        self.bd = BD()
        self._config_name = config_name
        self._pin_enable = None
        self._pin_direction = None
        self._pin_steps = None
        self._name = None
        self._simulated = None
        self._direction = None
        self._velocity = None
        self._steps = None
        self._vr_init = None
        self._vr_end = None
        self._cur_pos = None
        self._image_prefix = None
        
    @property
    def pin_enable(self):
        self._pin_enable = self.bd.config.get(self._config_name, 'pin_enable')
        return self._pin_enable

    @pin_enable.setter
    def pin_enable(self, value):
        self.bd.write(self._config_name, 'pin_enable', value)
        self._pin_enable = value

    @property
    def pin_direction(self):
        self._pin_direction = self.bd.config.get(self._config_name, 'pin_direction')
        return self._pin_direction

    @pin_direction.setter
    def pin_direction(self, value):
        self.bd.write(self._config_name, 'pin_direction', value)
        self._pin_direction = value

    @property
    def pin_steps(self):
        self._pin_steps = self.bd.config.get(self._config_name, 'pin_steps')
        return self._pin_steps

    @pin_steps.setter
    def pin_steps(self, value):
        self.bd.write(self._config_name, 'pin_steps', value)
        self._pin_steps = value

    @property
    def name(self):
        self._name = self.bd.config.get(self._config_name, 'name')
        return self._name

    @name.setter
    def name(self, value):
        self.bd.write(self._config_name, 'name', value)
        self._name = value

    @property
    def simulated(self):
        self._simulated = self.bd.config.getboolean(self._config_name, 'simulated')
        return self._simulated

    @simulated.setter
    def simulated(self, value):
        self.bd.write(self._config_name, 'simulated', value)
        self._simulated = value

    @property
    def direction(self):
        self._direction = self.bd.config.get(self._config_name, 'direction')
        return self._direction

    @direction.setter
    def direction(self, value):
        self.bd.write(self._config_name, 'direction', value)
        self._direction = value

    @property
    def velocity(self):
        self._velocity = self.bd.config.getint(self._config_name, 'velocity')
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self.bd.write(self._config_name, 'velocity', value)
        self._velocity = value

    @property
    def steps(self):
        self._steps = self.bd.config.getint(self._config_name, 'steps')
        return self._steps

    @steps.setter
    def steps(self, value):
        self.bd.write(self._config_name, 'steps', value)
        self._steps = value

    @property
    def vr_init(self):
        self._vr_init = self.bd.config.getint(self._config_name, 'vr_init')
        return self._vr_init

    @vr_init.setter
    def vr_init(self, value):
        self.bd.write(self._config_name, 'vr_init', value)
        self._vr_init = value

    @property
    def vr_end(self):
        self._vr_end = self.bd.config.getint(self._config_name, 'vr_end')
        return self._vr_end

    @vr_end.setter
    def vr_end(self, value):
        self.bd.write(self._config_name, 'vr_end', value)
        self._vr_end = value

    @property
    def cur_pos(self):
        self._cur_pos = self.bd.config.get(self._config_name, 'cur_pos')
        return self._cur_pos

    @cur_pos.setter
    def cur_pos(self, value):
        self.bd.write(self._config_name, 'cur_pos', value)
        self._cur_pos = value

    @property
    def image_prefix(self):
        self._image_prefix = self.bd.config.get(self._config_name, 'image_prefix')
        return self._image_prefix

    @image_prefix.setter
    def image_prefix(self, value):
        self.bd.write(self._config_name, 'image_prefix', value)
        self._image_prefix = value

class Star(object):
    def __init__(self, star):
        self.bd = BD()
        self._config_name = "led_%d" % star
        self._pin_led = None
        self._pin_group = None
        self._pin_enable = None
        self._name = None
        self._simulated = None
        self._exp_time = None
        self._brightness = None
        self._image_prefix = None

    @property
    def pin_led(self):
        self._pin_led = self.bd.config.get(self._config_name, 'pin_led')
        return self._pin_led

    @pin_led.setter
    def pin_led(self, value):
        self.bd.write(self._config_name, 'pin_led', value)
        self._pin_led = value
        
    @property
    def pin_group(self):
        self._pin_group = self.bd.config.get(self._config_name, 'pin_group')
        return self._pin_group

    @pin_group.setter
    def pin_group(self, value):
        self.bd.write(self._config_name, 'pin_group', value)
        self._pin_group = value
        
    @property
    def pin_enable(self):
        self._pin_enable = self.bd.config.get(self._config_name, 'pin_enable')
        return self._pin_enable

    @pin_enable.setter
    def pin_enable(self, value):
        self.bd.write(self._config_name, 'pin_enable', value)
        self._pin_enable = value
        
    @property
    def name(self):
        self._name = self.bd.config.get(self._config_name, 'name')
        return self._name

    @name.setter
    def name(self, value):
        self.bd.write(self._config_name, 'name', value)
        self._name = value
        
    @property
    def simulated(self):
        self._simulated = self.bd.config.getboolean(self._config_name, 'simulated')
        return self._simulated

    @simulated.setter
    def simulated(self, value):
        self.bd.write(self._config_name, 'simulated', value)
        self._simulated = value
        
    @property
    def exp_time(self):
        self._exp_time = self.bd.config.getfloat(self._config_name, 'exp_time')
        return self._exp_time

    @exp_time.setter
    def exp_time(self, value):
        self.bd.write(self._config_name, 'exp_time', value)
        self._exp_time = value

    @property
    def brightness(self):
        self._brightness = self.bd.config.getint(self._config_name, 'brightness')
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self.bd.write(self._config_name, 'brightness', value)
        self._brightness = value
        
    @property
    def image_prefix(self):
        self._image_prefix = self.bd.config.get(self._config_name, 'image_prefix')
        return self._image_prefix

    @image_prefix.setter
    def image_prefix(self, value):
        self.bd.write(self._config_name, 'image_prefix', value)
        self._image_prefix = value

class BeagleDarcServerM(object):
    def __init__(self, config_name):
        self.bd = BD()
        self._config_name = config_name
        self._host = None
        self._user = None
        self._password = None
        self._port = None

    @property
    def host(self):
        self._host = self.bd.config.get(self._config_name, 'host')
        return self._host

    @host.setter
    def host(self, value):
        self.bd.write(self._config_name, 'host', value)
        self._host = value

    @property
    def user(self):
        self._user = self.bd.config.get(self._config_name, 'user')
        return self._user

    @user.setter
    def user(self, value):
        self.bd.write(self._config_name, 'user', value)
        self._user = value

    @property
    def password(self):
        self._password = self.bd.config.get(self._config_name, 'password')
        return self._password

    @password.setter
    def password(self, value):
        self.bd.write(self._config_name, 'password', value)
        self._password = value

    @property
    def port(self):
        self._port = self.bd.config.get(self._config_name, 'port')
        return self._port

    @port.setter
    def port(self, value):
        self.bd.write(self._config_name, 'port', value)
        self._port = value

class Darc(object):
    def __init__(self, config_name):
        self.bd = BD()
        self._config_name = config_name
        self._camera = None
        self._pxlx = None 
        self._pxly = None 
        self._image_path = None
        self._image_path_dir = None

    @property
    def camera(self):
        self._camera = self.bd.config.get(self._config_name, 'camera')
        return self._camera

    @camera.setter
    def camera(self, value):
        self.bd.write(self._config_name, 'camera', value)
        self._camera = value

    @property
    def pxlx(self):
        self._pxlx = self.bd.config.get(self._config_name, 'pxlx')
        return self._pxlx

    @pxlx.setter
    def pxlx(self, value):
        self.bd.write(self._config_name, 'pxlx', value)
        self._pxlx = value

    @property
    def pxly(self):
        self._pxly = self.bd.config.get(self._config_name, 'pxly')
        return self._pxly

    @pxly.setter
    def pxly(self, value):
        self.bd.write(self._config_name, 'pxly', value)
        self._pxly = value

    @property
    def image_path(self):
        self._image_path = self.bd.config.get(self._config_name, 'image_path')
        return self._image_path

    @image_path.setter
    def image_path(self, value):
        self.bd.write(self._config_name, 'image_path', value)
        self._image_path = value

    @property
    def image_path_dir(self):
        return self._image_path_dir

    @image_path_dir.setter
    def image_path_dir(self, value):
        current =  str(time.strftime("%Y_%m_%d", time.gmtime()))
        current_dir = glob.glob(self._image_path+'*')
        current_dir = sorted(current_dir)
        last = current_dir[-1]
        if last.split('/')[-1].split('.')[0] == current:
            adquisition_number = int(last.split('/')[-1].split('.')[1]) + 1
            dir_name = current+'.'+ str(adquisition_number)
        else:
            dir_name = current+'.0'
        self._image_path_dir = dir_name


if __name__ == '__main__':
    #m = BD()
    pass
    
