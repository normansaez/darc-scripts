import logging
import unittest

class BBBTest(unittest.TestCase):
    '''
    '''
    def setUp(self):
        '''
        '''
        pass

    def tearDown(self):
        '''
        '''
        pass

    def test_import(self):
        '''
        '''
        message = ""
        try:
            import BeagleDarc
        except Exception, e:
            message = e.message
        self.assertNotEqual('No module named BeagleDarc', message)
        ##########################################################
        try:
            from BeagleDarc.Peripherals import Motor
        except Exception, e:
            message = e.message
        self.assertNotEqual('cannot import name motor', message)
        ##########################################################
        try:
            from BeagleDarc.Peripherals import Led
        except Exception, e:
            message = e.message
        self.assertNotEqual('cannot import name led', message)

    def test_intanciate_motor(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        self.assertRaises(NameError,Motor,'dummy_name')
        m = Motor('ground_layer')
        self.assertEqual (m.__class__.__name__,'Motor')
        m = Motor('horizontal_altitude_layer')
        self.assertEqual (m.__class__.__name__,'Motor')
        m = Motor('vertical_altitude_layer')
        self.assertEqual (m.__class__.__name__,'Motor')
        ####################

    def test_intanciate_led(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        n_min = 0
        n_max = 55

        for led in range(0,66):
            if led <= n_min:
                self.assertRaises(NameError, Led, led)
            elif led > n_max: 
                self.assertRaises(NameError, Led, led)
            else:
                l = Led(led)
                self.assertEqual (l.__class__.__name__,'Led')
        ####################

    def test_led_simulated(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        l = Led(1)

        in_val = True
        out_val = False
        l.set_simulated(in_val)
        out_val = l.get_simulated()
        self.assertEqual(in_val, out_val)

    def test_led_pin(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        l = Led(1)

        in_val = 1
        out_val = 0
        l.set_pin(in_val)
        out_val = l.get_pin()
        self.assertEqual(in_val, out_val)

    def test_led_name(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        l = Led(1)

        in_val = 'name'
        out_val = ''
        l.set_name(in_val)
        out_val = l.get_name()
        self.assertEqual(in_val, out_val)

    def test_led_exp_time(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        l = Led(1)

        in_val = 10
        out_val = 0
        l.set_exp_time(in_val)
        out_val = l.get_exp_time()
        self.assertEqual(in_val, out_val)

    def test_led_brightness(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        l = Led(1)

        in_val = 10
        out_val = 0
        l.set_brightness(in_val)
        out_val = l.get_brightness()
        self.assertEqual(in_val, out_val)

    def test_led_brightness(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        l = Led(1)

        in_val = 10
        out_val = 0
        l.set_brightness(in_val)
        out_val = l.get_brightness()
        self.assertEqual(in_val, out_val)

    def test_led_on(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        l = Led(1)
        self.assertEqual (l.__class__.__name__,'Led')
        l.set_on()
        ####################

    def test_led_off(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        l = Led(1)
        self.assertEqual (l.__class__.__name__,'Led')
        l.set_off()
        ####################
#-----------------------------------------------------------------------
    def test_motor_simulated(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')

        in_val = True
        out_val = False
        m.set_simulated(in_val)
        out_val = m.get_simulated()
        self.assertEqual(in_val, out_val)

    def test_motor_name(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')

        in_val = 'name'
        out_val = ''
        m.set_name(in_val)
        out_val = m.get_name()
        self.assertEqual(in_val, out_val)

    def test_motor_pin(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')

        in_val = 1
        out_val = 0
        m.set_pin(in_val)
        out_val = m.get_pin()
        self.assertEqual(in_val, out_val)

    def test_cur_pos(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')

        in_val = 1
        out_val = 0
        m.set_cur_pos(in_val)
        out_val = m.get_cur_pos()
        self.assertEqual(in_val, out_val)

    def test_steps(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')

        in_val = 1
        out_val = 0
        m.set_steps(in_val)
        out_val = m.get_steps()
        self.assertEqual(in_val, out_val)


    def test_direction(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')

        in_val = 1
        out_val = 0
        m.set_direction(in_val)
        out_val = m.get_direction()
        self.assertEqual(in_val, out_val)


    def test_velocity(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')

        in_val = 1
        out_val = 0
        m.set_velocity(in_val)
        out_val = m.get_velocity()
        self.assertEqual(in_val, out_val)

    def test_vr_init(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')

        in_val = 1
        out_val = 0
        m.set_vr_init(in_val)
        out_val = m.get_vr_init()
        self.assertEqual(in_val, out_val)

    def test_vr_end(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')

        in_val = 1
        out_val = 0
        m.set_vr_end(in_val)
        out_val = m.get_vr_end()
        self.assertEqual(in_val, out_val)

    def test_move_motor_with_sensor(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')
        cur_pos = 0 
        cur_pos = m.move_motor_with_sensor(cur_pos)
        cmd_pos = 1000 
        cur_pos = m.move_motor_with_sensor(cmd_pos)
        self.assertEqual(cur_pos, cmd_pos)

    def test_move_motor_skip_sensor(self):
        '''
        '''
        from BeagleDarc.Peripherals import Motor
        m = Motor('ground_layer')
        cur_pos = 0 
        cur_pos = m.move_motor_skip_sensor(cur_pos)
        cmd_pos = 1000 
        cur_pos = m.move_motor_skip_sensor(cmd_pos)
        self.assertEqual(cur_pos, cmd_pos)

    def test_get_pin(self):
        from BeagleDarc.Model import Model
        m = Model()
        p = m.get_star_pin()
        self.assertEqual("P8_8", p)

    def test_set_pin(self):
        from BeagleDarc.Model import Model
        m = Model()
        p = m.get_star_pin()
        p2 = "P8_4"
        m.set_star_pin(value=p2)
        self.assertNotEqual(p, p2)
        m.set_star_pin(value=p)
        p2 = m.get_star_pin()
        self.assertEqual(p, p2)

if __name__ == '__main__':
    bbbt = unittest.TestLoader().loadTestsFromTestCase(BBBTest)
#    bbbt = unittest.TestSuite()
#    bbbt.addTest(BBBTest('test_import'))
#    bbbt.addTest(BBBTest('test_intanciate_motor'))

    ##############################################################
    allsuites = unittest.TestSuite([bbbt])
    unittest.TextTestRunner(verbosity=2).run( allsuites )

