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

    def test_led_on(self):
        '''
        '''
        from BeagleDarc.Peripherals import Led
        l = Led(1)
        self.assertEqual (l.__class__.__name__,'Led')
        l.set_on()
        ####################

if __name__ == '__main__':
    bbbt = unittest.TestLoader().loadTestsFromTestCase(BBBTest)
#    bbbt = unittest.TestSuite()
#    bbbt.addTest(BBBTest('test_import'))
#    bbbt.addTest(BBBTest('test_intanciate_motor'))

    ##############################################################
    allsuites = unittest.TestSuite([bbbt])
    unittest.TextTestRunner(verbosity=2).run( allsuites )

