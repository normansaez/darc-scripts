#!/usr/bin/python 
'''
BoardDarcController
This script controls the board and communicates with darc to take an image
'''
import sys
sys.path.append('/rtc/lib/python')

import os
import re
import time
import glob
import serial
import logging
import random
import ConfigParser

import darc
import FITS

from optparse import OptionParser
from subprocess import Popen, PIPE

__package__ = 'BoardDarcController'

#COLOR CONST
BLUE     = '\033[34m'
RED      = '\033[31m'
GREEN    = '\033[32m'
YELLOW   = '\033[33m'
BLACK    = '\033[30m'
CRIM     = '\033[36m'
NO_COLOR = '\033[0m'

MILI2SEC  = 1e-3
MOTOR_CTE = 1.5e-3*0

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
        Config = ConfigParser.ConfigParser()
        self.Config = Config
        self.led = None
        self.exposicion = None
        self.brillo = None
        self.image_prefix = None
        
        self.motor = None
        self.pasos = None
        self.velocidad = None
        self.direccion = None
        self.dir_name = None
        self.delay = 0.5
        try:
            self.Config.read("/home/dani/nsaez/board/configurations.cfg")
            #self.Config.read("configurations.cfg")
        except:
            logging.error("configurations.cfg : File doesn't exits")
            sys.exit(-1)
        try:
            self.tty = find_usb_tty()[0]
            self._execute_cmd('sudo chmod 777 %s' % self.tty)
            logging.info("USB connected: %s" % self.tty)
            self.pic = serial.Serial(self.tty) 
            self.pic.port = "/dev/ttyUSB1"
            self.pic.baudrate = 9600
            self.pic.bytesize = serial.EIGHTBITS #number of bits per bytes
            self.pic.parity = serial.PARITY_NONE #set parity check: no parity
            self.pic.stopbits = serial.STOPBITS_ONE #number of stop bits
            self.pic.timeout = None          #block read
            #self.pic.timeout = 0             #non-block read
            #self.pic.timeout = 2              #timeout block read
            self.pic.xonxoff = False     #disable software flow control
            self.pic.rtscts = False     #disable hardware (RTS/CTS) flow control
            self.pic.dsrdtr = False       #disable hardware (DSR/DTR) flow control
            #self.pic.writeTimeout = 2     #timeout for write
            self.pic.writeTimeout = None     #block write
            self.pic.open()
            #check http://pyserial.sourceforge.net/pyserial_api.html
            logging.info("USB <--> PIC using python")
        except Exception, ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(ex)
            logging.error("Seems to be unplugged usb cable to pic ! or connecting with PIC")
            logging.error("Check line number: %d" % exc_tb.tb_lineno)
            sys.exit(-1)
        try:
            self.camera_name = self.Config.get('darc', 'camera')
            self.pxlx  = self.Config.getint('darc',  'pxlx')
            self.pxly  = self.Config.getint('darc', 'pxly')
            self.image_path  = self.Config.get('darc', 'image_path')
            self.darc = darc.Control(self.camera_name)
        except Exception, ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(ex)
            logging.error("Check line number: %d" % (exc_tb.tb_lineno))
            sys.exit(-1)
    def __del__(self):
        '''
        Destructor
        '''
        self.pic.close()

    def _execute_cmd(self, cmd):
        ''' 
        Execute console commands.
        return status, output and error messages
        '''
        process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
        sts = process.wait()
        out = process.stdout.read().strip()
        err = process.stderr.read().strip()
        logging.debug("cmd: "+str(cmd))
        logging.debug("sts: "+str(sts))
        if str(out).__contains__("Error"):
            logging.error("out: "+str(out))
            logging.error("err: "+str(err))
        else:
            logging.debug("out: "+str(out))
            logging.debug("err: "+str(err))

        return sts, out, err

    def _get_response(self):
        '''
        Get response from PIC
        '''
        numOfLines = 0
        while True:
            response = self.pic.readline()
            #logging.debug("read data: " + response)
            print "read data: " + response
            numOfLines = numOfLines + 1
            if (numOfLines >= 5):
                break
        return response

    def set_led_on(self):
        '''
        Method to turn on a led with no specific time. To turn off a led,
        set_led_off method needs to be called. Specific led is taken from
        configuration file. To overwrite it, use set_led(led) method.
        '''
        self.pic.write("1")
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Led %d ON" % self.led)

    def set_led_off(self):
        '''
        Method to turn off all leds. Period.
        '''
        self.pic.write("2")
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Led %d OFF" % self.led)

    def set_motor_move(self):
        '''
        Method to move a motor, using steps (pasos) and direction (direccion).
        Specific motor, step and direction is taken from configuration file. To
        overwrite it, use set_motor(motor), set_pasos(steps) and
        set_direccion(direction)
        '''
        self.pic.write("3")
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Motor %d pasos: %d, direccion %d" %(self.motor, self.pasos, self.direccion))
        logging.info('Waiting: %.2f [secs]'% (self.pasos*MOTOR_CTE))
        time.sleep(self.pasos*MOTOR_CTE)

    def set_led_on_off(self):
        '''
        Method to turn on/off a led for a exposure time. Specific led, and
        exposure time is taken from configuration file. To overwrite it, use
        set_led(led) and set_exposicion(time) methods.
        '''
        self.pic.write("4")
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Led %d, exposicion %d [ms]" % (self.led, self.exposicion))
        time.sleep(self.exposicion*MILI2SEC)

    def move_motor_with_vel(self):
        '''
        Method to move a motor, using steps (pasos) and direction (direccion)
        and a velocity (velocidad) Specific motor, step, direction and velocity
        is taken from configuration file. To overwrite it, use
        set_motor(motor), set_pasos(steps) , set_direccion(direction)
        set_velocidad(velocity) methods
        '''
        self.pic.write("5")
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Motor %d, velocidad %d" % (self.motor, self.velocidad))
        logging.info('Waiting: %.2f [secs]'% (self.pasos*MOTOR_CTE))
        time.sleep(self.pasos*MOTOR_CTE)

    def move_motor_with_sensor(self):
        '''
        '''
        logging.info("Motor %d, velocidad %d" % (self.motor, self.velocidad))
        self.pic.write("6")
        time.sleep(self.delay)
        out = self._get_response()
        time.sleep(self.pasos*MOTOR_CTE)

    def move_motor_skip_sensor(self):
        '''
        '''
        logging.info("Motor %d, velocidad %d" % (self.motor, self.velocidad))
        self.pic.write("7")
        time.sleep(self.delay)
        out = self._get_response()
        time.sleep(self.pasos*MOTOR_CTE)

    def set_led(self, led):
        '''
        Set led to be used in PIC. This method overwrite the default
        configuration taken from configuration file.
        '''
        self.led = led
        self.pic.write("l")
        time.sleep(self.delay)
        self.pic.write("%d\r" % led)
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Setting Led %d done" % led)
    
    def set_exposicion(self, exposicion):
        '''
        Set exposure time to be used on a specific led on PIC. This method
        overwrite the default configuration taken from configuration file.
        '''
        self.exposicion = exposicion
        self.pic.write("e")
        time.sleep(self.delay)
        self.pic.write("%d\r" % exposicion)
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Setting exposicion %d [ms] done" % exposicion)

    def set_brillo(self, brillo):
        '''
        Sets PWV function from 0 - 100 to simulate brightness in PIC. This
        method overwrite the default configuration taken from configuration
        file.
        '''
        self.brillo = brillo
        self.pic.write("b")
        time.sleep(self.delay)
        self.pic.write("%d\r" % brillo)
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Setting brillo %d done" % brillo)

    def set_motor(self, motor):
        '''
        Set motor to be used in PIC. This method overwrite the default
        configuration taken from configuration file
        '''
        self.motor = motor
        self.pic.write("m")
        time.sleep(self.delay)
        self.pic.write("%d\r" % motor)
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Setting motor %d done" % motor)

    def set_direccion(self, direccion):
        '''
        Set motor direction to be used in PIC. This method overwrite the
        default configuration taken from configuration file
        '''
        self.direccion = direccion
        self.pic.write("d")
        time.sleep(self.delay)
        self.pic.write("%d\r" % direccion)
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Setting direccion %d done" % direccion)

    def set_velocidad(self, velocidad):
        '''
        Set motor velocity to be used in PIC (this is a delay between 200 - 400
        ms). This method overwrite the default configuration taken from
        configuration file
        '''
        self.velocidad = velocidad
        self.pic.write("v")
        time.sleep(self.delay)
        self.pic.write("%d\r" % velocidad)
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Setting velocidad %d done" % velocidad)

    def set_pasos(self, pasos):
        '''
        Set motor steps to be used in PIC. This method overwrite the default
        configuration taken from configuration file
        '''
        self.pasos = pasos
        self.pic.write("p")
        time.sleep(self.delay)
        self.pic.write("%d\r" % pasos)
        time.sleep(self.delay)
        out = self._get_response()
        logging.info("Setting pasos %d done" % pasos)
        
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
        logging.info('Directory name: %s'% dir_name)
        return dir_name

    def take_img_from_darc(self, iteration, prefix):
        '''
        Using darc, take a FITS image and save it into the disk. By default use
        a image_prefix-YEAR-MONTH-DAY-T-HOUR-MIN-SEC.fits as image name.  The
        path to be store the file as well as image_prefix can be modified in
        configuration file
        '''
        try:
            logging.debug('About to take image with darc ...')
            stream = self.darc.GetStream(self.camera_name+'rtcPxlBuf')
            img_ite = 's%s_'% str(iteration).zfill(3)
            img_wfs = 'w%s_'% str(prefix).zfill(3)
            image_name = img_ite + img_wfs +'T' +str(time.strftime("%Y_%m_%dT%H_%M_%S.fits", time.gmtime()))
            if os.path.exists(self.image_path+self.dir_name) is False:
                os.mkdir(self.image_path+self.dir_name)
            path = os.path.normpath(self.image_path+self.dir_name+'/'+image_name)
            logging.info('Image taken : %s' % path)
            logging.debug(stream)
            data = stream[0].reshape(self.pxly,self.pxlx)
            data = data.view('h')
            logging.debug('About to save image to disk , name: %s' % path)
            FITS.Write(data, path, writeMode='a')
            logging.info('Image saved : %s' % path)
        except Exception, ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(ex)
            logging.error("Check line number: %d" % exc_tb.tb_lineno)
            logging.error("Is darc running??") 

    def setup(self, config_name='led_lgs1'):
        '''
        Setup default parameters taken from configurations.cfg
        '''
        logging.info('Configuring :%s ' % config_name)
        if config_name.__contains__('led'):
            led = self.Config.getint(config_name, 'led')
            exposicion = self.Config.getint(config_name, 'exposicion')
            brillo = self.Config.getint(config_name, 'brillo')
            self.image_prefix  = self.Config.get(config_name, 'image_prefix')

            self.set_led(led)
            self.set_exposicion(exposicion)
            self.set_brillo(brillo)

        if config_name.__contains__('motor'):
            motor = self.Config.getint(config_name, 'motor')
            direccion = self.Config.getint(config_name, 'direccion')
            velocidad = self.Config.getint(config_name, 'velocidad')
            pasos = self.Config.getint(config_name, 'pasos')
            self.set_motor(motor)
            self.set_direccion(direccion)
            self.set_velocidad(velocidad)
            self.set_pasos(pasos)
        logging.info('Configuration :%s done!' % config_name)


    def loop_for_r0(self):
        '''
        Loop to calculate r0. Move a motor forever.
        '''
        self.setup('motor_ground_layer')
        self.set_pasos(2147483600) 
        self.move_motor_with_sensor()

    def led_lgs1(self):
        '''
        Turn on/off a led, for test purposes.
        '''
        self.setup('led_lgs1')
        self.set_led_on()
        time.sleep(self.exposicion*MILI2SEC)
        self.set_led_off()
    def led_lgs2(self):
        '''
        Turn on/off a led, for test purposes.
        '''
        self.setup('led_lgs2')
        self.set_led_on()
        time.sleep(self.exposicion*MILI2SEC)
        self.set_led_off()

    def led_lgs3(self):
        '''
        Turn on/off a led, for test purposes.
        '''
        self.setup('led_lgs3')
        self.set_led_on()
        time.sleep(self.exposicion*MILI2SEC)
        self.set_led_off()

    def led_sci(self):
        '''
        Turn on/off a led, for test purposes.
        '''
        self.setup('led_sci')
        self.set_led_on()
        time.sleep(self.exposicion*MILI2SEC)
        self.set_led_off()

    def motor_alt_vertical(self):
        '''
        Turn on/off a led, for test purposes.
        '''
        self.setup('motor_alt_vertical')
        self.move_motor_with_vel()

    def motor_alt_horizontal(self):
        '''
        Turn on/off a led, for test purposes.
        '''
        self.setup('motor_alt_horizontal')
        self.move_motor_with_vel()

    def motor_ground_layer(self):
        '''
        Turn on/off a led, for test purposes.
        '''
        self.setup('motor_ground_layer')
        self.move_motor_with_vel()

    def calibration(self):
        '''
        Calibrate motors
        '''
        msg ='''
        Press 1 to calibrate: motor_ground_layer
        Press 2 to calibrate: motor_alt_vertical
        Press 3 to calibrate: motor_alt_horizontal
        '''
        m = 'motor_ground_layer'
        motor = raw_input(msg)
        motor_dir ={1:'motor_ground_layer',2:'motor_alt_vertical',3:'motor_alt_horizontal'}
        try:
            m = motor_dir[int(motor)]
        except Exception, ex:
            logging.error(RED+"Please put an allowed number: 1,2 or 3"+NO_COLOR)

        self.setup(m)
        logging.info(GREEN+'Moving until find a sensor'+NO_COLOR)
        self.set_pasos(2147483600) 
        self.move_motor_with_sensor()
        #################################
        logging.info(GREEN+'Skipping from sensor'+NO_COLOR)
        self.set_pasos(2000) 
        if self.direccion == 1:
            self.set_direccion(0)
        else:
            self.set_direccion(1)
        self.move_motor_skip_sensor()
        if self.direccion == 1:
            self.set_direccion(0)
        else:
            self.set_direccion(1)
        #################################
        msg = '''
        Please put steps
        '''
        steps = int(raw_input(msg))
        all_steps = 0
        valid_step_init = 0
        valid_step_end  = 0
        full_range = 0

        self.set_pasos(steps)
        while (True):
            self.move_motor_skip_sensor()
            all_steps = all_steps + steps
            if valid_step_init == 0:
                print "Is this a valid init range? [y/n]"
                valid= raw_input()
                if valid == 'y':
                    valid_step_init = all_steps
                    print "valid_step_init :%d" % valid_step_init
            valid = 'n'

            if valid_step_end == 0 and valid_step_init > 0:
                print "Is this a valid end range? [y/n]"
                valid= raw_input()
                if valid == 'y':
                    valid_step_end = all_steps
                    print "valid_step_end :%d" % valid_step_end
                
            valid = 'n'
            if full_range == 0 and valid_step_init > 0 and valid_step_end > 0:
                print "Is this the end of the path? [y/n]"
                valid= raw_input()
                if valid == 'y':
                    full_range = all_steps
                    print "full_range :%d" % full_range
            if full_range > 0 and valid_step_init > 0 and valid_step_end > 0:
                break
        #################################
        logging.info(GREEN+'Skipping from sensor'+NO_COLOR)
        self.set_pasos(2000) 
        if self.direccion == 1:
            self.set_direccion(0)
        else:
            self.set_direccion(1)
        self.move_motor_skip_sensor()
        if self.direccion == 1:
            self.set_direccion(0)
        else:
            self.set_direccion(1)
        #################################
        logging.info(GREEN+'Back to original position'+NO_COLOR)
        self.set_pasos(full_range) 
        self.move_motor_with_sensor()
        #################################
        logging.info(GREEN+'Skipping from sensor'+NO_COLOR)
        self.set_pasos(2000) 
        if self.direccion == 1:
            self.set_direccion(0)
        else:
            self.set_direccion(1)
        self.move_motor_skip_sensor()
        if self.direccion == 1:
            self.set_direccion(0)
        else:
            self.set_direccion(1)
        #################################
        logging.info(GREEN+'Calibration DONE'+NO_COLOR)
        logging.info(GREEN+('valid_step_init: %d' % valid_step_init)+NO_COLOR)
        logging.info(GREEN+('valid_step_end : %d' % valid_step_end)+NO_COLOR)
        logging.info(GREEN+('full_range     : %d' % full_range)+NO_COLOR)

    def table(self, num, israndom=False):
        '''
        This method does:
        0. take image (dark)
        1. turn on led 1
        2. take image
        3. turn on led 2
        4. take image
        5. turn on led 3
        6. take image
        7. move a motor
        
        After that,  start all over again,  given a number of times in num
        variable
        '''
        self.dir_name = self.get_directory(self.image_path)
        self.take_img_from_darc('dark', 'dark')
        for iteration in range(0, num):
            self.setup('led_lgs1')
            # led 1 on
            self.set_led_on()
            time.sleep(self.exposicion*MILI2SEC)

            #take img with darc
            self.take_img_from_darc(iteration, self.image_prefix)

            #led off
            self.set_led_off()

            # led 2 on
            self.setup('led_lgs2')
            self.set_led_on()
            time.sleep(self.exposicion*MILI2SEC)

            #take img with darc
            self.take_img_from_darc(iteration, self.image_prefix)

            #led off
            self.set_led_off()

            # led 3 on
            self.setup('led_lgs3')
            self.set_led_on()
            time.sleep(self.exposicion*MILI2SEC)

            #take img with darc
            self.take_img_from_darc(iteration, self.image_prefix)

            #led off
            self.set_led_off()

            # sci led on
            self.setup('led_sci')
            self.set_led_on()
            time.sleep(self.exposicion*MILI2SEC)

            #take img with darc
            self.take_img_from_darc(iteration, self.image_prefix)

            #led off
            self.set_led_off()

            #mover motores:
            if israndom is True:
                self.pasos = random.randint(1e2, 1e3)
                self.setup('motor_alt_horizontal')
                self.move_motor_with_vel()
                time.sleep(self.pasos*MOTOR_CTE)
                #####################################
                self.pasos = random.randint(1e2, 1e3)
                self.setup('motor_alt_vertical')
                self.move_motor_with_vel()
                time.sleep(self.pasos*MOTOR_CTE)
            else:
                #mover motores:
                self.setup('motor_alt_horizontal')
                self.move_motor_with_vel()
                #XXX to be fixed , espera 60 seg hasta que el motor se mueva por
                #que no se maneja el return desde el pic. Deberia esperar la
                #respuesta final del pic para poder seguir moviendo.  Soluciones: en
                #el return del pic enviar una senal EOF en cada funcion y esperar
                #desde el codigo send_receive_pic hasta esta funcion. Con esto se
                #soluciona el problema, pero no esta implementado.
                time.sleep(self.pasos*MOTOR_CTE)

########### funcion auxiliar ########################################
def find_usb_tty(vendor_id = None, product_id = None):
    '''
    find_usb_tty: used to get the correct /dev/ttyUSB*
    Not included in BoardControlled class
    '''
    tty_devs    = []

    for dn in glob.glob('/sys/bus/usb/devices/*') :
        try     :
            vid = int(open(os.path.join(dn, "idVendor" )).read().strip(), 16)
            pid = int(open(os.path.join(dn, "idProduct")).read().strip(), 16)
            if  ((vendor_id is None) or (vid == vendor_id)) and ((product_id is None) or (pid == product_id)) :
                dns = glob.glob(os.path.join(dn, os.path.basename(dn) + "*"))
                for sdn in dns :
                    for fn in glob.glob(os.path.join(sdn, "*")) :
                        if  re.search(r"\/ttyUSB[0-9]+$", fn) :
                            #tty_devs.append("/dev" + os.path.basename(fn))
                            tty_devs.append(os.path.join("/dev", os.path.basename(fn)))
                        pass
                    pass
                pass
            pass
        except ( ValueError, TypeError, AttributeError, OSError, IOError ) :
            pass
        pass
    return tty_devs

#####################################################################
############################# MAIN ##################################
#####################################################################

if __name__ == '__main__':
    usage = '''
        BoardDarcController <options>
        Check /home/dani/nsaez/board/configurations.cfg default configurations
            Type -h, --help for help.
                '''
    parser = OptionParser(usage)
    parser.add_option("-r", "--r0", dest="r0", metavar="r0", default=False, action="store_true", help = "Start loop to obtain r0 (infinite loop)")
    parser.add_option("-t", "--table", dest="table", metavar="table", default=False, action="store_true", help = "Movement needed for table")
    parser.add_option("-a", "--aleatory", dest="aleatory", metavar="aleatory", default=False, action="store_true", help = "Movement needed for table, aleatory motor_alt_vertical, motor_alt_horizontal")
    parser.add_option("-n", "--num", dest="num", metavar="num", type="int", default=2, help = "Number of iterations for --table method")
    parser.add_option("-c", "--calibration", dest="calibration", metavar="calibration", default=False, action="store_true", help = "Calibration method for MOTORS")
    parser.add_option("-1", "--led_lgs1", dest="led_lgs1", metavar="led_lgs1", default=False, action="store_true", help = "Test, turning on/off led_lgs1")
    parser.add_option("-2", "--led_lgs2", dest="led_lgs2", metavar="led_lgs2", default=False, action="store_true", help = "Test, turning on/off led_lgs2")
    parser.add_option("-3", "--led_lgs3", dest="led_lgs3", metavar="led_lgs3", default=False, action="store_true", help = "Test, turning on/off led_lgs3")
    parser.add_option("-s", "--led_sci", dest="led_sci", metavar="led_sci", default=False, action="store_true", help = "Test, turning on/off led_sci")
    parser.add_option("-v", "--motor_alt_vertical", dest="motor_alt_vertical", metavar="motor_alt_vertical", default=False, action="store_true", help = "Test, turning on/off motor_alt_vertical")
    parser.add_option("-o", "--motor_alt_horizontal", dest="motor_alt_horizontal", metavar="motor_alt_horizontal", default=False, action="store_true", help = "Test, turning on/off motor_alt_horizontal")
    parser.add_option("-g", "--motor_ground_layer", dest="motor_ground_layer", metavar="motor_ground_layer", default=False, action="store_true", help = "Test, turning on/off motor_ground_layer")
    parser.add_option("-d", "--debug", dest="debug", metavar="debug", default=False, action="store_true", help = "debug mode, prints all messages")
    (options , args) = parser.parse_args()
    if options.debug is False:
        logging.getLogger().setLevel(logging.INFO)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')

    if options.r0 is False and \
    options.table is False and \
    options.led_lgs1 is False and \
    options.led_lgs2 is False and \
    options.led_lgs3 is False and \
    options.led_sci is False and \
    options.calibration is False and \
    options.motor_alt_vertical is False and \
    options.motor_alt_horizontal is False and \
    options.aleatory is False and \
    options.motor_ground_layer is False:
        print usage
        print "It is mandatory use --r0 , --table, --calibration or --ledtest as parameter"
        sys.exit(-1)

    BDC = BoardDarcController()
    if options.r0 is True:
        BDC.loop_for_r0()

    if options.table is True:
        BDC.table(options.num)

    if options.aleatory is True:
        BDC.table(options.num, israndom=True)

    if options.calibration is True:
        BDC.calibration()

    if options.motor_ground_layer is True:
        BDC.motor_ground_layer()

    if options.motor_alt_vertical is True:
        BDC.motor_alt_vertical()

    if options.motor_alt_horizontal is True:
        BDC.motor_alt_horizontal()

    if options.led_lgs1 is True:
        BDC.led_lgs1()

    if options.led_lgs2 is True:
        BDC.led_lgs2()

    if options.led_lgs3 is True:
        BDC.led_lgs3()

    if options.led_sci is True:
        BDC.led_sci()

