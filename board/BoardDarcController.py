#!/usr/bin/python 
'''
BoardDarcController:
Controla Board y Darc desde el mismo script
'''
import ConfigParser
import sys

from subprocess import Popen, PIPE
from time import sleep
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
            print "No se encontro el archivo configurations.cfg, asegurese de que esta en el mismo directorio"
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
            print ex
            print "revisar linea: %d" % exc_tb.tb_lineno
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

    def loop_for_r0(self):
        '''
        Loop de calibracion para phase screens
        '''
        pass

    def setup(self):
        '''
        Setup antes de enviar cualquier ejecucion de comandos
        '''
        cmd = "send_receive_pic /dev/ttyUSB0 l"
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % self.led_num
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        print "Setting led %d done" % self.led_num
        
        cmd = "send_receive_pic /dev/ttyUSB0 e"
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % self.exposicion
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        print "Setting exposicion %d done" % self.exposicion

        cmd = "send_receive_pic /dev/ttyUSB0 b"
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % self.brillo
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        print "Setting brillo %d done" % self.exposicion


        cmd = "send_receive_pic /dev/ttyUSB0 m"
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % self.motor_num
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        print "Setting motor %d done" % self.motor_num


        cmd = "send_receive_pic /dev/ttyUSB0 d"
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % self.direccion
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        print "Setting direccion %d done" % self.direccion


        cmd = "send_receive_pic /dev/ttyUSB0 v"
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % self.velocidad
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        print "Setting velocidad %d done" % self.velocidad


        cmd = "send_receive_pic /dev/ttyUSB0 p"
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        cmd = "send_receive_pic /dev/ttyUSB0 %d\n" % self.pasos
        sts, out, err = self._execute_cmd(cmd)
        sleep(self.delay)
        print "Setting pasos %d done" % self.pasos

        print "Setting loop instead pasos: %r" % self.loop

if __name__ == '__main__':
    BDC = BoardDarcController()
    BDC.setup()
