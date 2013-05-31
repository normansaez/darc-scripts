#!/usr/bin/python 
'''
BoardDarcController
This script controls the board and communicates whith darc to take an image
'''
import ConfigParser
import sys
import logging

from optparse import OptionParser
from subprocess import Popen, PIPE
from time import sleep
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
class BoardDarcController:
    '''
    BoardDarcController:
    This script controls the board and communicates whith darc to take an image
    '''
    def __init__(self):
        '''
        Takes parameters configured in configurations.cfg file
        path:
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
            self.delay = Config.getfloat('other','delay')

        except Exception, ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(ex)
            logging.error("Check line number: %d" % exc_tb.tb_lineno)
            sys.exit(-1)

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
        Turn led on , it is mandatory set a led first
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 1"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Led %d ON" % self.led)

    def set_led_off(self):
        '''
        Turn led off.
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 2"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Led %d OFF" % self.led)

    def set_motor_move(self):
        '''
        The motor moves given steps and direction
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 3"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Motor %d pasos: %d, direccion %d" % (self.motor, self.pasos, self.direccion))

    def set_led_on_off(self):
        '''
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 4"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Led %d exposicion %d" % (self.led, self.exposicion))

    def move_motor_with_vel(self):
        '''
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 5"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Motor %d, velocidad %d" % (self.motor, self.velocidad))

    def move_motor_forever(self):
        '''
        '''
        logging.info("Motor %d, velocidad %d" % (self.motor, self.velocidad))
        logging.info("Forever")
        cmd = "send_receive_pic /dev/ttyUSB0 5"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)

    def set_led(self, led):
        '''
        Set led to be used in PIC
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 l"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % led
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Setting led %d done" % led)
    
    def set_exposicion(self, exposicion):
        '''
        Set exposition time to be used on a specific led on PIC
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 e"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % exposicion
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Setting exposicion %d done" % exposicion)

    def set_brillo(self, brillo):
        '''
        Sets PWV function from 0 - 100 to simulate brigthness in PIC
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 b"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % brillo
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Setting brillo %d done" % brillo)

    def set_motor(self,motor):
        '''
        Set motor to be used in PIC
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 m"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % motor
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Setting motor %d done" % motor)

    def set_direccion(self, direccion):
        '''
        Set motor direction to be used in PIC
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 d"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % direccion
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Setting direccion %d done" % direccion)

    def set_velocidad(self, velocidad):
        '''
        Set motor velocity to be used in PIC (this is a delay between 200 - 400 ms)
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 v"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % velocidad
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Setting velocidad %d done" % velocidad)

    def set_pasos(self, pasos):
        '''
        Set motor steps to be used in PIC
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 p"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % pasos
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)
        logging.info("Setting pasos %d done" % pasos)

    def set_delay(self, delay):
        logging.info("Setting delay entre instrucciones al pic: %f" % delay)
        
    def setup(self):
        '''
        Setup with default parameters taken from configurations.cfg
        '''
        self.set_led(self.led)
        self.set_exposicion(self.exposicion)
        self.set_brillo(self.brillo)
        self.set_motor(self.motor)
        self.set_direccion(self.direccion)
        self.set_velocidad(self.velocidad)
        self.set_pasos(self.pasos)
        self.set_delay(self.delay)

    def loop_for_r0(self):
        '''
        Loop for r0
        '''
        self.setup()
        cmd = "send_receive_pic /dev/ttyUSB0 6"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)

    def table(self,num_image):
        '''
        turn start by start, then move phase screen, and repeat
        '''
        self.setup()
        for i in range(0,num_image):
            # led 1 on
            self.set_led(1)
            self.set_led_on()
            sleep(self.exposicion)

            #capturar img con darc

            #led off
            self.set_led_off()

            # led 2 on
            self.set_led(2)
            self.set_led_on()
            sleep(self.exposicion)

            #capturar img con darc

            #led off
            self.set_led_off()

            # led 3 on
            self.set_led(3)
            self.set_led_on()
            sleep(self.exposicion)

            #capturar img con darc

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
    parser.add_option("-r", "--r0", dest="r0", metavar="r0", default=False, action="store_true", help = "Star loop to obtain r0 (infinite loop)")
    parser.add_option("-m", "--table", dest="table", metavar="table", default=False, action="store_true", help = "Movement needed for table")
    parser.add_option("-v", "--verbose", dest="verbose", metavar="verbose", default=False, action="store_true", help = "debug mode, prints all messages")
    (options , args) = parser.parse_args()
    if options.verbose is False:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.DEBUG)

    if options.r0 is False and options.table is False:
        print usage
        print "It is mandatory use --r0 or --table as parameter"
        sys.exit(-1)

    BDC = BoardDarcController()
    if options.r0 is True:
        BDC.loop_for_r0()

    if options.table is True:
        BDC.table(2)
