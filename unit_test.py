import unittest
from lsl_emulator import start_lsl
import biostream_v2
from multiprocessing import Process

class TestBioStream(unittest.TestCase):

    # *** Initialization Unit Tests... ***
    #def setUp(self):
     lsl_error =  "LSL device not connected:"
     serial_error = "Serial Port not connected:"

    # *** Run Data Collection Unit Tests... ***
    #tests should start with "test_" in order to be considered

    # *** tests for LSL only *** #
    def test_lslnotconnected(self):
        with self.assertRaisesRegex(ValueError, lsl_error):
            biostream_v2.main_test()
         
    def test_lsldisconnection(self):
        lsl_emulator_process = Process(target=start_lsl)
        biostream_process = Process(target=  biostream_v2.main_test())
        lsl_emulator_process.start()
        with self.assertRaisesRegex(ValueError, lsl_error):
            biostream_process.start()
            time.sleep(100)
            lsl_emulator_process.terminate()
            biostream_process.join()

   # def test_numberofsamples(self):

    
    
    # *** tests for LSL and Knee Encoder (serial device) *** #
    def test_lslnotconnected_2(self):
        with self.assertRaisesRegex(ValueError, lsl_error):
            biostream_v2.main_test()

    def test_serialnotconnected(self):
        lsl_emulator = Process(target= start_lsl)
        lsl_emulator.start()
        with self.assertRaisesRegex(ValueError, serial_error):
            biostream_v2.main_test()
        lsl_emulator.terminate()
    
    """
    def test_lsldisconnection_2(self):
    
    def test_serialdisconnection(self):
    
    def test_numberofsamples_2(self):
    """

if __name__ == '__main__':
   unittest.main()