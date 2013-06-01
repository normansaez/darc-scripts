#!/usr/bin/python 
'''
BoardDarcController
This script controls the board and communicates with darc to take an image
'''
import ConfigParser
import sys
import logging
import os

#import FITS
#import darc
import time
import numpy

from optparse import OptionParser
from subprocess import Popen, PIPE
from time import sleep

__package__ = 'BoardDarcController'

class BoardDarcController:
    '''
    BoardDarcController:
    This script controls the board and communicates with darc to take an image
    '''
    def __init__(self):
        '''
        Sets parameters taken from configurations.cfg file.
        The current path for configuration file is:
        /home/dani/nsaez/board/configurations.cfg
        '''
        try:
            Config = ConfigParser.ConfigParser()
            Config.read("/home/dani/nsaez/board/configurations.cfg")
        except:
            logging.error("configurations.cfg : File doesn't exits")
            sys.exit(-1)
        try:
            self.led = Config.getint('led', 'led')
            self.exposicion = Config.getint('led', 'exposicion')
            self.brillo = Config.getint('led', 'brillo')
            self.motor = Config.getint('motor', 'motor')
            self.direccion = Config.getint('motor', 'direccion')
            self.velocidad = Config.getint('motor', 'velocidad')
            self.pasos = Config.getint('motor', 'pasos')
            self.pxlx  = Config.getint('darc', 'pxlx')
            self.pxly  = Config.getint('darc', 'pxly')
            self.image_prefix  = Config.get('darc', 'image_prefix')
            self.image_path  = Config.get('darc', 'image_path')
        except Exception, ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(ex)
            logging.error("Check line number: %d" % exc_tb.tb_lineno)
            sys.exit(-1)
        try:
            self.camera_name = Config.get('darc','camera')
            self.darc = darc.Control(self.camera_name)
        except Exception, ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
#            logging.error(ex)
#            logging.error("Check line number: %d" % exc_tb.tb_lineno)
#            sys.exit(-1)

    def _execute_cmd(self, cmd):
        ''' 
        Execute console commands.
        return status, output and error messages
        '''
        process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
        sts = process.wait()
        out = process.stdout.read().strip()
        err = process.stderr.read().strip()
        return sts, out, err

    def set_led_on(self):
        '''
        Method to turn on a led with no specific time. To turn off a led,
        set_led_off method needs to be called. Specific led is taken from
        configuration file. To overwrite it, use set_led(led) method.
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 1 :"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Led %d ON" % self.led)

    def set_led_off(self):
        '''
        Method to turn off all leds. Period.
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 2 :"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Led %d OFF" % self.led)

    def set_motor_move(self):
        '''
        Method to move a motor, using steps (pasos) and direction (direccion).
        Specific motor, step and direction is taken from configuration file. To
        overwrite it, use set_motor(motor), set_pasos(steps) and
        set_direccion(direction)
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 3 :"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Motor %d pasos: %d, direccion %d" % (self.motor, self.pasos, self.direccion))

    def set_led_on_off(self):
        '''
        Method to turn on/off a led for a exposure time. Specific led, and
        exposure time is taken from configuration file. To overwrite it, use
        set_led(led) and set_exposicion(time) methods.
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 4 :"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Led %d exposicion %d" % (self.led, self.exposicion))

    def move_motor_with_vel(self):
        '''
        Method to move a motor, using steps (pasos) and direction (direccion)
        and a velocity (velocidad) Specific motor, step, direction and velocity
        is taken from configuration file. To overwrite it, use
        set_motor(motor), set_pasos(steps) , set_direccion(direction)
        set_velocidad(velocity) methods
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 5 :"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Motor %d, velocidad %d" % (self.motor, self.velocidad))

    def move_motor_forever(self):
        '''
        Method to move a motor, using steps (pasos) and direction (direccion)
        and a velocity (velocidad). The main difference with
        move_motor_with_vel method is that once the motor moves specific steps,
        it will start all over again (forever). The only way to stops motor is
        reseting PIC. Specific motor, step, direction and velocity is taken
        from configuration file. To overwrite it, use set_motor(motor),
        set_pasos(steps) , set_direccion(direction) set_velocidad(velocity)
        methods
        '''
        logging.info("Motor %d, velocidad %d" % (self.motor, self.velocidad))
        logging.info("Forever")
        cmd = "send_receive_pic /dev/ttyUSB0 6 :"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))

    def set_led(self, led):
        '''
        Set led to be used in PIC. This method overwrite the default
        configuration taken from configuration file.
        '''
        self.led = led
        cmd = "send_receive_pic /dev/ttyUSB0 l:%d\r :" % led
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Setting led %d done" % led)
    
    def set_exposicion(self, exposicion):
        '''
        Set exposure time to be used on a specific led on PIC. This method
        overwrite the default configuration taken from configuration file.
        '''
        self.exposicion = exposicion
        cmd = "send_receive_pic /dev/ttyUSB0 e:%d\r :" % exposicion
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Setting exposicion %d done" % exposicion)

    def set_brillo(self, brillo):
        '''
        Sets PWV function from 0 - 100 to simulate brightness in PIC. This
        method overwrite the default configuration taken from configuration
        file.
        '''
        self.brillo = brillo
        cmd = "send_receive_pic /dev/ttyUSB0 b:%d\r :" % brillo
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Setting brillo %d done" % brillo)

    def set_motor(self,motor):
        '''
        Set motor to be used in PIC. This method overwrite the default
        configuration taken from configuration file
        '''
        self.motor = motor
        cmd = "send_receive_pic /dev/ttyUSB0 m:%d\r :" % motor
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Setting motor %d done" % motor)

    def set_direccion(self, direccion):
        '''
        Set motor direction to be used in PIC. This method overwrite the
        default configuration taken from configuration file
        '''
        self.direccion = direccion
        cmd = "send_receive_pic /dev/ttyUSB0 d:%d\r :" % direccion
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.debug(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        logging.info("Setting direccion %d done" % direccion)

    def set_velocidad(self, velocidad):
        '''
        Set motor velocity to be used in PIC (this is a delay between 200 - 400
        ms). This method overwrite the default configuration taken from
        configuration file
        '''
        self.velocidad = velocidad
        cmd = "send_receive_pic /dev/ttyUSB0 v:%d\r :" % velocidad
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Setting velocidad %d done" % velocidad)

    def set_pasos(self, pasos):
        '''
        Set motor steps to be used in PIC. This method overwrite the default
        configuration taken from configuration file
        '''
        self.pasos = pasos
        cmd = "send_receive_pic /dev/ttyUSB0 p:%d\r :" % pasos
        sts, out, err = self._execute_cmd(cmd)
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        logging.debug("out: "+str(out))
        logging.debug("err: "+str(err))
        logging.info("Setting pasos %d done" % pasos)
        
    def take_img_from_darc(self):
        '''
        Using darc, take a FITS image and save it into the disk. By default use
        a image_prefix-YEAR-MONTH-DAY-T-HOUR-MIN-SEC.fits as image name.  The
        path to be store the file as well as image_prefix can be modified in
        configuration file
        '''
        try:
            logging.debug('About to take image with darc ...')
            #stream = self.darc.GetStream(self.camera_name+'rtcPxlBuf')
            image_name = self.image_prefix+'_' + str(time.strftime("%Y_%m_%dT%H_%M_%S.fits", time.gmtime()))
            path = os.path.normpath(self.image_path+image_name)
            logging.info('Image taken : %s' % path)
            #data = stream.reshape(self.pxly,self.pxlx)
            logging.debug('About to save image to disk , name: %s' % path)
            #FITS.Write(data, path, writeMode='a')
            logging.info('Image saved : %s' % path)
        except Exception, ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(ex)
            logging.error("Check line number: %d" % exc_tb.tb_lineno)
            logging.error("Is darc running??") 

    def setup(self):
        '''
        Setup default parameters taken from configurations.cfg
        '''
        self.set_led(self.led)
        self.set_exposicion(self.exposicion)
        self.set_brillo(self.brillo)
        self.set_motor(self.motor)
        self.set_direccion(self.direccion)
        self.set_velocidad(self.velocidad)
        self.set_pasos(self.pasos)


    def loop_for_r0(self):
        '''
        Loop to calculate r0. Move a motor forever.
        '''
        self.setup()
        #numero muy muy grande de pasos
        self.set_pasos(2147483600) 
        self.move_motor_forever()

    def ledtest(self):
        '''
        Turn on/off a led, for test purposes.
        '''
        self.setup()
        self.set_led_on_off()


    def table(self,num):
        '''
        This method does:
        (a) turn on led 1
        (b) take image
        (c) turn on led 2
        (d) take image
        (e) turn on led 3
        (f) take image
        (g) move a motor
        
        After that, start all over again, given a number of times in num
        variable
        '''
        self.setup()
        for i in range(0,num):
            # led 1 on
            self.set_led(1)
            self.set_led_on()
            sleep(self.exposicion)

            #take img with darc
            self.take_img_from_darc()

            #led off
            self.set_led_off()

            # led 2 on
            self.set_led(2)
            self.set_led_on()
            sleep(self.exposicion)

            #take img with darc
            self.take_img_from_darc()

            #led off
            self.set_led_off()

            # led 3 on
            self.set_led(3)
            self.set_led_on()
            sleep(self.exposicion)

            #take img with darc
            self.take_img_from_darc()

            #led off
            self.set_led_off()

            #mover motores:
            self.move_motor_with_vel()

if __name__ == '__main__':
    usage = '''
        BoardDarcController <options>
        Check /home/dani/nsaez/board/configurations.cfg default configurations
            Type -h, --help for help.
                '''
    parser = OptionParser(usage)
    parser.add_option("-r", "--r0", dest="r0", metavar="r0", default=False, action="store_true", help = "Start loop to obtain r0 (infinite loop)")
    parser.add_option("-t", "--table", dest="table", metavar="table", default=False, action="store_true", help = "Movement needed for table")
    parser.add_option("-n", "--num", dest="num", metavar="num", type="int", default=2, help = "Number of iterations for --table method")
    parser.add_option("-l", "--ledtest", dest="ledtest", metavar="ledtest", default=False, action="store_true", help = "Test, turning on/off a led")
    parser.add_option("-d", "--debug", dest="debug", metavar="debug", default=False, action="store_true", help = "debug mode, prints all messages")
    (options , args) = parser.parse_args()
    if options.debug is False:
        logging.getLogger().setLevel(logging.INFO)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')

    if options.r0 is False and options.table is False and options.ledtest is False:
        print usage
        print "It is mandatory use --r0 , --table or --ledtest as parameter"
        sys.exit(-1)

    BDC = BoardDarcController()
    if options.r0 is True:
        BDC.loop_for_r0()

    if options.table is True:
        BDC.table(options.num)

    if options.ledtest is True:
        BDC.ledtest()
