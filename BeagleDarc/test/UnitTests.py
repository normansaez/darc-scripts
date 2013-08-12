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
            from BeagleDarc import Motor
        except Exception, e:
            message = e.message
        self.assertNotEqual('cannot import name Motor', message)
        ##########################################################
        try:
            from BeagleDarc import Led
        except Exception, e:
            message = e.message
        self.assertNotEqual('cannot import name Led', message)

    def test_intanciate_motor(self):
        '''
        '''
        from BeagleDarc import Motor
        m = Motor('ground_layer')
        m = Motor('horizontal_altitude_layer')
        m = Motor('vertical_altitude_layer')
        ####################

if __name__ == '__main__':
#    bbbt = unittest.TestLoader().loadTestsFromTestCase(BBBTest)
    bbbt = unittest.TestSuite()
    bbbt.addTest(BBBTest('test_import'))
    bbbt.addTest(BBBTest('test_intanciate_motor'))

    ##############################################################
    allsuites = unittest.TestSuite([bbbt])
    unittest.TextTestRunner(verbosity=2).run( allsuites )

