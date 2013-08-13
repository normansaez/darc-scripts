import socket

'''
Peripherals
'''
class Device:
    '''
    Common methods to communicate with BeagleBone
    '''
    def __init__(self):
        self.pin = None
        self.name = None
        self.s = None
        self.simulated = False

    def connect(self):
        '''
        '''
        self.s = socket.socket()         
        host = socket.gethostname() 
        port = 12345         
        self.s.connect((host, port))

    def disconnect(self):
        '''
        '''
        self.s.close

    def send_and_wait(self, msg):
        self.connect()
        self.s.send(msg)
        while 1:
            response = self.s.recv(1024)
            #print response
            if response.__contains__("ack"):
                self.disconnect()
                break

class Motor(Device):
    '''
    Motor
    '''
    def __init__(self, name):
        '''
        Instanciate by name
        '''
        Device.__init__(self)
        valid_names = ['ground_layer', 'horizontal_altitude_layer', 'vertical_altitude_layer']
        if name in valid_names:
            self.name = name
            self.number = None
            self.cur_pos = None
            self.steps = None
            self.direction = None
            self.velocity = None
            self.vr_init = None
            self.vr_end = None
        else:
            msg = "Valid names are: ground_layer, horizontal_altitude_layer, vertical_altitude_layer , change: %s by a valid name" % name 
            raise NameError(msg)

class Led(Device):
    '''
    Led
    '''
    def __init__(self, number):
        '''
        Instanciate by number
        '''
        Device.__init__(self)
        n_min = 0
        n_max = 55
        if number > n_min and number <= n_max:
            self.number = number
            self.exp_time = None
            self.brightness = None
        else:
            msg = "Valid names are: %d to %d, change: %s by a valid name" % (n_min+1, n_max, number)
            raise NameError(msg)

    def set_on(self):
        '''
        ''' 
        self.send_and_wait('turn on')
        pass

    def set_off(self):
        '''
        '''
        pass

