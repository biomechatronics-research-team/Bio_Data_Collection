import unittest
from lsl_emulator import start_lsl
import biostream_v2
from multiprocessing import Process
from time import sleep

class TestBioStream(unittest.TestCase):

    lsl_error =  "LSL device not connected:"
    serial_error = "Serial Port not connected:"



    # *** Run Data Collection Unit Tests... ***
    #tests should start with "test_" in order to be considered

    # *** tests for LSL only *** #
    def test_lslnotconnected(self):
        biostream_process = Process(target=  biostream_v2.main_test)
        biostream_process.start()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 1)
       
    def test_lsldisconnection(self):
        lsl_emulator_process = Process(target=start_lsl)
        biostream_process = Process(target=  biostream_v2.main_test)
        lsl_emulator_process.start()
        biostream_process.start()
        sleep(1)
        lsl_emulator_process.terminate()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 3)

   # def test_numberofsamples(self):

    
    # *** tests for LSL and Knee Encoder (serial device) *** #
    # TODO -> Simulate serial device
    def test_lslnotconnected_2(self):
        biostream_process = Process(target= biostream_v2.main_test)
        biostream_process.start()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 1)

    def test_serialnotconnected(self):
        lsl_emulator = Process(target= start_lsl)
        lsl_emulator.start()
        biostream_process = Process(target=  biostream_v2.main_test)
        biostream_process.start()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 2)
        lsl_emulator.terminate()
    
    """
    def test_lsldisconnection_2(self):
    
    def test_serialdisconnection(self):
    
    def test_numberofsamples_2(self):
    """

if __name__ == '__main__':
   unittest.main()