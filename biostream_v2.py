from pylsl import StreamInlet, resolve_byprop, LostError
from serial import Serial
from serial.tools import list_ports
from multiprocessing import Process, Queue
from time import time


class BioStream:
    '''
        This class defines the behavior for the data collection process performed
        by the Biomechatronics Research Group. It receives data from an OpenBCI
        Mark IV headset via LSL. It synchronizes the readings from OpenBCI with
        the measures from a custom device that sends data via serial corresponding
        to the knee angle of the patient.
        @author Pedro Luis Rivera Gomez
    '''

    # Defining inner 'wrapper' classes.

    class SensorData:
        '''
            This class represents a 2-tuple for a sensor data entry.
            It stores the sensor value along with its corresponding timestamp.
        '''

        def __init__(self, value, timestamp):
            self.value = value
            self.timestamp = timestamp

    class Mark4_Entry:
        '''
            This class represents a 2-tuple for an OpenBCI Mark IV headset entry.
            It stores the 8-channels values along with their corresponding timestamp.
        '''

        def __init__(self, channels, timestamp):
            self.channels = channels
            self.timestamp = timestamp

    # Default Biostream constructor. Initialize variables for data synchronization.
    def __init__(self):
        self.mark4entries_queue = Queue()
        self.kneeangle_queue = Queue()

    def find_lsl_index(self, stream_name):
        # Find EEG streams that are using the Lab Streaming Layer.
        self.streams = resolve_byprop('type', 'EEG', timeout = 0.5) 

        # Validate if stream_name is connected.
        stream_index = -1
        for i in range(0, len(self.streams)):
            if stream_name == self.streams[i].name():
                stream_index = i

        return stream_index

    # Defining data collection methods.

    # TODO -> Test this method...
    def collect_mark4lsl(self, num_samples, lsl_name):

        stream_index = self.find_lsl_index(lsl_name)
        if stream_index < 0:
            exit(1)

        # Create a new inlet to read from the stream_name.
        self.inlet = StreamInlet(self.streams[stream_index], recover= False)
        headset_entries = []

        while num_samples > 0:
            try:
                bci_sample = self.inlet.pull_sample()
            except LostError:
                exit(3)
            
            headset_entries.append(self.Mark4_Entry(bci_sample, time()))
            num_samples -= 1

        return headset_entries

    # Stores LSL entries resulting from the 'collect_mark4lsl' method into a Queue instance.
    def store_mark4lsl_entries(self, num_samples, lsl_name, queue):
        queue.put(self.collect_mark4lsl(num_samples, lsl_name))

    # TODO -> Implement & test this function.
    def collect_sensor_data(self, serial_name, baud_rate, num_samples):

        # TODO -> This part is not validating. Must fix this...
        # Validate if serial_port is connected.
        is_connected = False
        for device in list_ports.comports():
            print(device.usb_info)
            if device.device == serial_name:
                is_connected = True
                break

        if not is_connected:
            exit(2) 

        # Establish serial communication.
        self.serial_device = Serial(serial_name, baudrate=baud_rate)

        # Initialize sensor entries list.
        sensor_entries = []

        while num_samples > 0:
            # Get the latest sensor data.
            sensor_value = self.serial_device.readline().decode('ascii')
            sensor_timestamp = time()
            sensor_entries.append(self.SensorData(
                sensor_timestamp, sensor_value))
            num_samples -= 1
        return sensor_entries

    def store_sensor_entries(self, num_samples, serial_name, baud_rate, queue):
        queue.put(self.collect_sensor_data(
            serial_name, baud_rate, num_samples))

    # TODO -> Test this function and check if any other validation must be performed.
    def sync_headset_knee_data(self, bci_samples, knee_samples):

        if 2 * len(bci_samples) != len(knee_samples):
            raise Exception("Samples cardinality does not match.")

        sync_data = []

        for i in range(0, len(bci_samples)):
            # Get samples of interest.
            bci_sample = bci_samples[i]
            knee_sample_1 = knee_samples[2 * i]
            knee_sampple_2 = knee_samples[2 * i + 1]
            # Add the bci sample along with the average between both sensor values.
            sync_data.append((bci_sample, self.SensorData(
                timestamp=(knee_sample_1.timestamp+knee_sampple_2.timestamp)/2,
                value=((knee_sample_1.value+knee_sampple_2.value)/2)
            )))

        return sync_data

    # TODO -> Test this function and update design doc.
    def collect_mark4lsl_kneeserial(self, num_samples, lsl_name, serial_name, baud_rate):

        # Defining processes.
        mark4lsl_process = Process(
            target=self.store_mark4lsl_entries, args=(num_samples, lsl_name, self.mark4entries_queue))
        kneeangle_process = Process(target=self.store_sensor_entries, args=(
            2 * num_samples, serial_name, baud_rate, self.kneeangle_queue))

        # Start and join both processes.
        mark4lsl_process.start()
        kneeangle_process.start()
        mark4lsl_process.join()
        kneeangle_process.join()
        if mark4lsl_process.exitcode:
            #raise ValueError("LSL device not connected:", lsl_name)
            exit(mark4lsl_process.exitcode)
        if kneeangle_process.exitcode:
            #raise ValueError("Serial Port not connected:", serial_name)
            exit(kneeangle_process.exitcode)
        # TODO -> Synchronize data stored in these queues.
        #print(self.mark4entries_queue.get())
        #print(self.kneeangle_queue.get())

        return self.sync_headset_knee_data(self.mark4entries_queue.get(), self.kneeangle_queue.get())

def main_test(): 
    # Prepairing Mock Test.
    num_samples = 20
    lsl_name = "BioSemi"
    serial_name = "COM4"  # /dev/ttys012
    baud_rate = 9600

    # Initializing mock BioStream.
    mock = BioStream()


    # # Mock testing the data collection methods.
    # data_mark4 = mock.collect_mark4lsl(num_samples, lsl_name)
    # data_mark4_knee = mock.collect_mark4lsl_kneeserial(
    #     num_samples, lsl_name, serial_name, baud_rate)

    # # Displaying Mark4 results.
    # print("Mark4:", data_mark4)
    # for val in data_mark4:
    #     print(val.channels)

    # # Displaying Mark4 + Knee Angle results.
    # print("Mark4 + Knee Angle:", data_mark4_knee)
    data_mark5 = mock.collect_mark4lsl_kneeserial(
        num_samples, lsl_name, serial_name, baud_rate)
    # print(mock._tosync_mark4_entries)
    return 0

# Make sure Serial & LSL mock streams are running before running this file.
if __name__ == '__main__':
    main_test()
