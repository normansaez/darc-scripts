#!/usr/bin/python 
'''
Model
Handle file configurations between GUI/Controller
'''
import sys

import time
import glob
import logging
import ConfigParser


class Model:
    '''
    Model:
    Handle file configurations between GUI/Controller
    '''
    def __init__(self, configfile='/Users/nsaez/darc-scripts/BeagleDarc/BeagleDarc/configurations.cfg'):
        '''
        Sets parameters taken from configurations.cfg file.
        The current path for configuration file is:
        /home/dani/nsaez/board/configurations.cfg
        '''
        self.config = ConfigParser.ConfigParser()
        logging.basicConfig()
        self.log = logging.getLogger("Model")
        try:
            self.configfile = configfile
            self.config.read(self.configfile)
        except Exception, ex:
            _ , _ , exc_tb = sys.exc_info()
            self.log.error(ex)
            self.log.error("Check line number: %d" % (exc_tb.tb_lineno))
            self.log.error("configurations.cfg : File doesn't exits")
            sys.exit(-1)

    def __del__(self):
        pass 

    def get_directory(self, image_path):
        '''
        Set image directory name to take images
        return a string with these image directory
        '''
        current =  str(time.strftime("%Y_%m_%d", time.gmtime()))
        current_dir = glob.glob(image_path+'*')
        current_dir = sorted(current_dir)
        last = current_dir[-1]
        if last.split('/')[-1].split('.')[0] == current:
            adquisition_number = int(last.split('/')[-1].split('.')[1]) + 1
            dir_name = current+'.'+ str(adquisition_number)
        else:
            dir_name = current+'.0'
        self.log.info('Directory name: %s'% dir_name)
        return dir_name
    #beagledarc_server
    def get_beagledarc_server_host(self, config_name='beagledarc_server'):
        '''
        Get beagledarc_server host
        '''
        self.log.debug('Get beagledarc_server host from :%s ' % config_name)
        host = self.config.get(config_name, 'host')
        self.log.debug('Return :%s ' % host)
        return host

    def get_beagledarc_server_user(self, config_name='beagledarc_server'):
        '''
        Get beagledarc_server user
        '''
        self.log.debug('Get beagledarc_server user from :%s ' % config_name)
        user = self.config.get(config_name, 'user')
        self.log.debug('Return :%s ' % user)
        return user

    def get_beagledarc_server_password(self, config_name='beagledarc_server'):
        '''
        Get beagledarc_server password
        '''
        self.log.debug('Get beagledarc_server password from :%s ' % config_name)
        password = self.config.get(config_name, 'password')
        self.log.debug('Return :%s ' % password)
        return password

    def get_beagledarc_server_port(self, config_name='beagledarc_server'):
        '''
        Get beagledarc_server port
        '''
        self.log.debug('Get beagledarc_server port from :%s ' % config_name)
        port = self.config.get(config_name, 'port')
        self.log.debug('Return :%s ' % port)
        return port


    #darc
    def get_darc_camera_name(self, config_name='darc'):
        '''
        Get camera name
        '''
        self.log.debug('Get camera_name from :%s ' % config_name)
        camera_name = self.config.get(config_name, 'camera')
        self.log.debug('Return :%s ' % camera_name)
        return camera_name

    def get_darc_pxlx(self, config_name='darc'):
        '''
        Get pixel X for camera
        '''
        self.log.debug('Get pxlx from :%s ' % config_name)
        pxlx  = self.config.getint(config_name,  'pxlx')
        self.log.debug('Return :%s ' % pxlx)
        return pxlx

    def get_darc_pxly(self, config_name='darc'):
        '''
        Get pixel Y for camera
        '''
        self.log.debug('Get pxly from :%s ' % config_name)
        pxly  = self.config.getint(config_name, 'pxly')
        self.log.debug('Return :%s ' % pxly)
        return pxly

    def get_darc_image_path(self, config_name='darc'):
        '''
        Get image path
        '''
        self.log.debug('Get image_path from :%s ' % config_name)
        image_path  = self.config.get(config_name, 'image_path')
        self.log.debug('Return :%s ' % image_path)
        return image_path

    #star
    def get_star_pin(self, config_name='led_1'):
        '''
        Get star pin
        '''
        self.log.debug('Get pin from :%s ' % config_name)
        pin        = self.config.get(config_name, 'pin')
        self.log.debug('Return :%s ' % pin)
        return pin

    def get_star_name(self, config_name='led_1'):
        '''
        Get star name
        '''
        self.log.debug('Get name from :%s ' % config_name)
        name       = self.config.get(config_name, 'name')
        self.log.debug('Return :%s ' % name)
        return name

    def get_star_simulated(self, config_name='led_1'):
        '''
        Get if star is simulated
        '''
        self.log.debug('Get simulated from :%s ' % config_name)
        simulated  = self.config.getboolean(config_name, 'simulated')
        self.log.debug('Return :%s ' % simulated)
        return simulated

    def get_star_exp_time(self, config_name='led_1'):
        '''
        Get star expouse time
        '''
        self.log.debug('Get exp_time from :%s ' % config_name)
        exp_time   = self.config.getint(config_name, 'exp_time')
        self.log.debug('Return :%s ' % exp_time)
        return exp_time

    def get_star_brightness(self, config_name='led_1'):
        '''
        Get star brightness
        '''
        self.log.debug('Get brightness from :%s ' % config_name)
        brightness = self.config.getint(config_name, 'brightness')
        self.log.debug('Return :%s ' % brightness)
        return brightness

    def get_star_image_prefix(self, config_name='led_1'):
        '''
        Get star image prefix
        '''
        self.log.debug('Get image_prefix from :%s ' % config_name)
        image_prefix  = self.config.get(config_name, 'image_prefix')
        self.log.debug('Return :%s ' % image_prefix)
        return image_prefix

    #Motor
    def get_motor_pin(self, config_name='ground_layer'):
        '''
        Get motor pin
        '''
        self.log.debug('Get pin from :%s ' % config_name)
        pin  = self.config.get(config_name, 'pin')
        self.log.debug('Return :%s ' % pin)
        return pin

    def get_motor_name(self, config_name='ground_layer'):
        '''
        Get motor name
        '''
        self.log.debug('Get name from :%s ' % config_name)
        name = self.config.get(config_name, 'name')
        self.log.debug('Return :%s ' % name)
        return name

    def get_motor_simulated(self, config_name='ground_layer'):
        '''
        Get if motor is simulated
        '''
        self.log.debug('Get simulated from :%s ' % config_name)
        simulated = self.config.getboolean(config_name, 'simulated')
        self.log.debug('Return :%s ' % simulated)
        return simulated

    def get_motor_direction(self, config_name='ground_layer'):
        '''
        Get motor direction
        '''
        self.log.debug('Get direction from :%s ' % config_name)
        direction = self.config.get(config_name, 'direction')
        self.log.debug('Return :%s ' % direction)
        return direction

    def get_motor_velocity(self, config_name='ground_layer'):
        '''
        Get motor velocity
        '''
        self.log.debug('Get velocity from :%s ' % config_name)
        velocity = self.config.getint(config_name, 'velocity')
        self.log.debug('Return :%s ' % velocity)
        return velocity

    def get_motor_steps(self, config_name='ground_layer'):
        '''
        Get motor steps
        '''
        self.log.debug('Get steps from :%s ' % config_name)
        steps = self.config.getint(config_name, 'steps')
        self.log.debug('Return :%s ' % steps)
        return steps

    def get_motor_vr_init(self, config_name='ground_layer'):
        '''
        Get motor valid range init
        '''
        self.log.debug('Get vr_init from :%s ' % config_name)
        vr_init = self.config.getint(config_name, 'vr_init')
        self.log.debug('Return :%s ' % vr_init)
        return vr_init

    def get_motor_vr_end(self, config_name='ground_layer'):
        '''
        Get motor valid range end
        '''
        self.log.debug('Get vr_end from :%s ' % config_name)
        vr_end = self.config.getint(config_name, 'vr_end')
        self.log.debug('Return :%s ' % vr_end)
        return vr_end

    def get_motor_image_prefix(self, config_name='ground_layer'):
        '''
        Get motor image prefix
        '''
        self.log.debug('Get image_prefix from :%s ' % config_name)
        image_prefix  = self.config.get(config_name, 'image_prefix')
        self.log.debug('Return :%s ' % image_prefix)
        return image_prefix

#SET
    #darc
    def set_darc_camera_name(self, config_name='darc', value=None):
        '''
        Set camera name
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set camera_name to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'camera', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_darc_pxlx(self, config_name='darc', value=None):
        '''
        Set pixel X for camera
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set pxlx to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name,  'pxlx', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_darc_pxly(self, config_name='darc', value=None):
        '''
        Set pixel Y for camera
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set pxly to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'pxly', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_darc_image_path(self, config_name='darc', value=None):
        '''
        Set image path
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set image_path to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'image_path', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    #star
    def set_star_pin(self, config_name='led_1', value=None):
        '''
        Set star pin
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set pin to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'pin', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_star_name(self, config_name='led_1', value=None):
        '''
        Set star name
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set name to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'name', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_star_simulated(self, config_name='led_1', value=None):
        '''
        Set if star is simulated
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set simulated to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'simulated', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_star_exp_time(self, config_name='led_1', value=None):
        '''
        Set star expouse time
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set exp_time to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'exp_time', str(value))
        self.config.write(cfgfile)
        cfgfile.close()
        
    def set_star_brightness(self, config_name='led_1', value=None):
        '''
        Set star brightness
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set brightness to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'brightness', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_star_image_prefix(self, config_name='led_1', value=None):
        '''
        Set star image prefix
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set image_prefix to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'image_prefix', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    #Motor
    def set_motor_pin(self, config_name='ground_layer', value=None):
        '''
        Set motor pin
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set pin to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'pin', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_motor_name(self, config_name='ground_layer', value=None):
        '''
        Set motor name
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set name to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'name', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_motor_simulated(self, config_name='ground_layer', value=None):
        '''
        Set if motor is simulated
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set simulated to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'simulated', str(value))
        self.config.write(cfgfile)
        cfgfile.close()
        
    def set_motor_direction(self, config_name='ground_layer', value=None):
        '''
        Set motor direction
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set direction to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'direction', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_motor_velocity(self, config_name='ground_layer', value=None):
        '''
        Set motor velocity
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set velocity to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'velocity', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_motor_steps(self, config_name='ground_layer', value=None):
        '''
        Set motor steps
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set steps to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'steps', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_motor_vr_init(self, config_name='ground_layer', value=None):
        '''
        Set motor valid range init
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set vr_init to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'vr_init', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_motor_vr_end(self, config_name='ground_layer', value=None):
        '''
        Set motor valid range end
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set vr_end to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'vr_end', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_motor_image_prefix(self, config_name='ground_layer', value=None):
        '''
        Set motor image prefix
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set image_prefix to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'image_prefix', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    #beagledarc_server
    def set_beagledarc_server_host(self, config_name='beagledarc_server', value=None):
        '''
        Set beagledarc_server host
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set beagledarc_server host to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'host', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_beagledarc_server_user(self, config_name='beagledarc_server', value=None):
        '''
        Set beagledarc_server user
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set beagledarc_server user to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'user', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_beagledarc_server_password(self, config_name='beagledarc_server', value=None):
        '''
        Set beagledarc_server password
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set beagledarc_server password to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'password', str(value))
        self.config.write(cfgfile)
        cfgfile.close()

    def set_beagledarc_server_port(self, config_name='beagledarc_server', value=None):
        '''
        Set beagledarc_server port
        '''
        cfgfile = open(self.configfile,'w')
        self.log.debug('Set beagledarc_server port to %s , value %s ' % (config_name, str(value)))
        self.config.set(config_name, 'port', str(value))
        self.config.write(cfgfile)
        cfgfile.close()


if __name__ == '__main__':
    pass
