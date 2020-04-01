import unittest
from lsl_emulator import start_lsl
from serial_emulator import start_serial
import biostream_v2
from multiprocessing import Process
from time import sleep

class TestBioStream(unittest.TestCase):

    """ *** Run Data Collection Unit Tests... 
    tests should start with "test_" in order to be considered """

    """ *** tests for LSL only *** """
    def test_lslnotconnected(self):
        biostream_process = Process(target=  biostream_v2.main_test)
        biostream_process.start()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 1)
       
    def test_lsldisconnection(self):
        lsl_emulator_process = Process(target=start_lsl)
        biostream_process = Process(target= biostream_v2.main_test)
        lsl_emulator_process.start()
        biostream_process.start()
        sleep(1)
        lsl_emulator_process.terminate()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 3)

    #def test_numberofsamples(self):

    
    """ *** tests for LSL and Knee Encoder (serial device) *** """
    def test_lslnotconnected_2(self):
        serial_emulator_process = Process(target= start_serial)
        biostream_process = Process(target= biostream_v2.main_test)
        serial_emulator_process.start()
        biostream_process.start()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 1)
        serial_emulator_process.terminate()

    def test_serialnotconnected(self):
        lsl_emulator_process = Process(target= start_lsl)
        lsl_emulator_process.start()
        biostream_process = Process(target=  biostream_v2.main_test)
        biostream_process.start()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 2)
        lsl_emulator_process.terminate()
    
    def test_lsldisconnection_2(self):
        lsl_emulator_process = Process(target=start_lsl)
        serial_emulator_process = Process(target= start_serial)
        biostream_process = Process(target= biostream_v2.main_test)
        lsl_emulator_process.start()
        serial_emulator_process.start()
        biostream_process.start()
        sleep(1)
        lsl_emulator_process.terminate()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 3)
        serial_emulator_process.terminate()
    
    def test_serialdisconnection(self):
        lsl_emulator_process = Process(target=start_lsl)
        serial_emulator_process = Process(target= start_serial)
        biostream_process = Process(target= biostream_v2.main_test)
        lsl_emulator_process.start()
        serial_emulator_process.start()
        biostream_process.start()
        sleep(1)
        serial_emulator_process.terminate()
        biostream_process.join()
        self.assertEqual(biostream_process.exitcode, 3)
        lsl_emulator_process.terminate()


    #def test_numberofsamples_2(self):
    

if __name__ == '__main__':
   unittest.main()