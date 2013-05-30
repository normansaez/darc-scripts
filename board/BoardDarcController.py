#!/usr/bin/python 
'''
BoardDarcController:
Controla Board y Darc desde el mismo script
'''
import ConfigParser
import sys
import logging

from optparse import OptionParser
from subprocess import Popen, PIPE
from time import sleep
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
class BoardDarcController:
    '''
    BoardDarcController:
    Controla Board y Darc desde el mismo script
    '''
    def __init__(self):
        '''
        Lee parametros de configuracion desde configurations.cfg
        '''
        try:
            Config = ConfigParser.ConfigParser()
            Config.read("/home/dani/nsaez/board/configurations.cfg")
        except:
            logging.error("No se encontro el archivo configurations.cfg, asegurese de que esta en el mismo directorio")
            sys.exit(-1)
        try:
            self.led_num = Config.getint('led', 'led')
            self.exposicion = Config.getint('led', 'exposicion')
            self.brillo = Config.getint('led', 'brillo')
            self.motor_num = Config.getint('motor', 'motor')
            self.direccion = Config.getint('motor', 'direccion')
            self.velocidad = Config.getint('motor', 'velocidad')
            self.pasos = Config.getint('motor', 'pasos')
            self.loop = Config.getboolean('motor', 'loop')
            self.delay = Config.getfloat('other','delay')

        except Exception, ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(ex)
            logging.error("revisar linea: %d" % exc_tb.tb_lineno)
            sys.exit(-1)

    def _execute_cmd(self, cmd):
        ''' 
        Ejecutar comandos por consola,
        retorna codestatus, stdout, stderr
        '''
        process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
        sts = process.wait()
        out = process.stdout.read().strip()
        err = process.stderr.read().strip()
        return sts, out, err

    def set_led(self, led):
        '''
        Set led in pic
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

    def set_loop(self, loop):
        logging.info("Setting loop instead pasos: %r" % loop)
        
    def setup(self):
        '''
        Setup antes de enviar cualquier ejecucion de comandos
        '''
        self.set_led(self.led_num)
        self.set_exposicion(self.exposicion)
        self.set_brillo(self.brillo)
        self.set_motor(self.motor_num)
        self.set_direccion(self.direccion)
        self.set_velocidad(self.velocidad)
        self.set_pasos(self.pasos)
        self.set_loop(self.loop)

    def loop_for_r0(self):
        '''
        Loop de calibracion para phase screens
        '''
        self.setup()
        cmd = "send_receive_pic /dev/ttyUSB0 6"
        sts, out, err = self._execute_cmd(cmd)
        logging.debug(sts)
        logging.debug(out)
        logging.debug(err)
        sleep(self.delay)

    def mesa(self,num_image):
        '''
        Loop de calibracion para phase screens
        '''
        self.setup()
        for i in range(0,num_image):
            # led 1 on
            self.set_led(1)
            cmd = "send_receive_pic /dev/ttyUSB0 1"
            sts, out, err = self._execute_cmd(cmd)
            logging.debug(sts)
            logging.debug(out)
            logging.debug(err)
            sleep(self.delay)
            sleep(self.exposicion)

            #capturar img con darc

            #led off
            cmd = "send_receive_pic /dev/ttyUSB0 2"
            sts, out, err = self._execute_cmd(cmd)
            logging.debug(sts)
            logging.debug(out)
            logging.debug(err)
            sleep(self.delay)

            # led 2 on
            self.set_led(2)
            cmd = "send_receive_pic /dev/ttyUSB0 1"
            sts, out, err = self._execute_cmd(cmd)
            logging.debug(sts)
            logging.debug(out)
            logging.debug(err)
            sleep(self.delay)
            sleep(self.exposicion)

            #capturar img con darc

            #led off
            cmd = "send_receive_pic /dev/ttyUSB0 2"
            sts, out, err = self._execute_cmd(cmd)
            logging.debug(sts)
            logging.debug(out)
            logging.debug(err)
            sleep(self.delay)

            # led 3 on
            self.set_led(3)
            cmd = "send_receive_pic /dev/ttyUSB0 1"
            sts, out, err = self._execute_cmd(cmd)
            logging.debug(sts)
            logging.debug(out)
            logging.debug(err)
            sleep(self.delay)
            sleep(self.exposicion)

            #capturar img con darc

            #led off
            cmd = "send_receive_pic /dev/ttyUSB0 2"
            sts, out, err = self._execute_cmd(cmd)
            logging.debug(sts)
            logging.debug(out)
            logging.debug(err)
            sleep(self.delay)

            #mover motores:
            cmd = "send_receive_pic /dev/ttyUSB0 5"
            sts, out, err = self._execute_cmd(cmd)
            logging.debug(sts)
            logging.debug(out)
            logging.debug(err)
            sleep(self.delay)
        
if __name__ == '__main__':
    usage = '''
        BoardDarcController <options>
        Check /home/dani/nsaez/board/configurations.cfg default configurations
            Type -h, --help for help.
                '''
    parser = OptionParser(usage)
    parser.add_option("-r", "--r0", dest="r0", metavar="r0", default=False, action="store_true", help = "Start calibracion r0 (loop infinito)")
    parser.add_option("-m", "--mesa", dest="mesa", metavar="mesa", default=False, action="store_true", help = "Movimientos para mesa, 40 imagenes by default")
    parser.add_option("-v", "--verbose", dest="verbose", metavar="verbose", default=False, action="store_true", help = "debug mode, con todos los printouts")
    (options , args) = parser.parse_args()
    if options.verbose is False:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.DEBUG)

    if options.r0 is False and options.mesa is False:
        print usage
        print "Necesita opcion --r0 o bien --mesa, con -h se obtiene informacion mas detallada"
        sys.exit(-1)

    BDC = BoardDarcController()
    if options.r0 is True:
        BDC.loop_for_r0()

    if options.mesa is True:
        BDC.mesa(40)
