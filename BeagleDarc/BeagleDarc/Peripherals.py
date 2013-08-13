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

    def set_pin(self, pin):
        '''
        '''
        self.pin = pin
    def set_name(self, name):
        '''
        '''
        self.name = name

    def set_simulated(self, simulated):
        '''
        '''
        self.simulated = simulated
#------------------------------------------------
    def get_pin(self):
        '''
        '''
        return self.pin

    def get_name(self):
        '''
        '''
        return self.name

    def get_simulated(self):
        '''
        '''
        return self.simulated

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
            self.cur_pos = None
            self.steps = None
            self.direction = None
            self.velocity = None
            self.vr_init = None
            self.vr_end = None
        else:
            msg = "Valid names are: ground_layer, horizontal_altitude_layer, vertical_altitude_layer , change: %s by a valid name" % name 
            raise NameError(msg)
#--------------------------------------------------
    def set_cur_pos(self, cur_pos):
        '''
        '''
        self.cur_pos = cur_pos

    def set_steps(self, steps):
        '''
        '''
        self.steps = steps

    def set_direction(self, direction):
        '''
        '''
        self.direction = direction

    def set_velocity(self, velocity):
        '''
        '''
        self.velocity = velocity

    def set_vr_init(self, vr_init):
        '''
        '''
        self.vr_init = vr_init

    def set_vr_end(self, vr_end):
        '''
        '''
        self.vr_end = vr_end
#----------------------------------------------------
    def get_cur_pos(self):
        '''
        '''
        return self.cur_pos

    def get_steps(self):
        '''
        '''
        return self.steps

    def get_direction(self):
        '''
        '''
        return self.direction

    def get_velocity(self):
        '''
        '''
        return self.velocity

    def get_vr_init(self):
        '''
        '''
        return self.vr_init

    def get_vr_end(self):
        '''
        '''
        return self.vr_end

####################################################################
    def set_on(self):
        '''
        ''' 
        self.send_and_wait('turn on')

    def set_off(self):
        '''
        '''
        self.send_and_wait('turn on')
############################################################################################################################################
class Led(Device):
    '''
    Led
    '''
    def __init__(self, pin):
        '''
        Instanciate by number
        '''
        Device.__init__(self)
        n_min = 0
        n_max = 55
        if pin > n_min and pin <= n_max:
            self.pin = pin
            self.exp_time = None
            self.brightness = None
        else:
            msg = "Valid names are: %d to %d, change: %s by a valid name" % (n_min+1, n_max, number)
            raise NameError(msg)

#--------------------------------------------------

    def set_exp_time(self, exp_time):
        '''
        '''
        self.exp_time = exp_time

    def set_brightness(self, brightness):
        '''
        '''
        self.brightness = brightness

#----------------------------------------------------
    def get_exp_time(self):
        '''
        '''
        return self.exp_time

    def get_brightness(self):
        '''
        '''
        return self.brightness



####################################################################
    def set_on(self):
        '''
        ''' 
        self.send_and_wait('turn on')

    def set_off(self):
        '''
        '''
        self.send_and_wait('turn on')


