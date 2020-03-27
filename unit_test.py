import unittest
from lsl_emulator import start_lsl
import biostream_v2
from multiprocessing import Process

class TestBioStream(unittest.TestCase):

    # *** Initialization Unit Tests... ***
    #def setUp(self):
        #lsl_emulator_process = Process(target=lsl_emulator.start_lsl)

    # *** Run Data Collection Unit Tests... ***
    #tests should start with "test_" in order to be considered

    # *** tests for LSL only *** #
    def test_lslnotconnected(self):
        with self.assertRaisesRegex(ValueError, "LSL device not connected:"):
            biostream_v2.main_test()
    """      
    def test_lsldisconnection(self):
        
    def test_numberofsamples(self):

    """
    
    # *** tests for LSL and Knee Encoder (serial device) *** #
    def test_lslnotconnected_2(self):
        with self.assertRaisesRegex(ValueError, "LSL device not connected:"):
            biostream_v2.main_test()

    def test_serialnotconnected(self):
        lsl_emulator = Process(target= start_lsl)
        lsl_emulator.start()
        with self.assertRaisesRegex(ValueError, "Serial Port not connected:"):
            biostream_v2.main_test()
        lsl_emulator.terminate()
    
    """
    def test_lsldisconnection_2(self):
    
    def test_serialdisconnection(self):
    
    def test_numberofsamples_2(self):
    """

if __name__ == '__main__':
   unittest.main()