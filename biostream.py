from pylsl import StreamInlet, resolve_stream
from serial import Serial, tools
from multiprocessing import Process
from time import time
from csv import DictWriter

class BioStream:
    """
        This class defines the behavior for the data collection process performed
        by the Biomechatronics Research Group. It receives data from an OpenBCI
        Mark IV headset via LSL. It synchronizes the readings from OpenBCI with
        the measures from a custom device that sends data via serial corresponding
        to the knee angle of the patient.
        @author Pedro Luis Rivera Gomez
    """

    # TODO -> Add the other parameters for the test...
    def __init__(self, stream_name, serial_port, baud_rate):
        # Find EEG streams that are using the Lab Streaming Layer.
        self.streams = resolve_stream('type', 'EEG')

        # Validate if stream_name is connected.
        stream_index = -1
        for i in range(0, len(self.streams)):
            if stream_name == self.streams[i].name():
                stream_index = i
        
        if stream_index < 0:
            raise ValueError("Stream not connected : %s" % stream_name)

        # Create a new inlet to read from the stream_name.
        self.inlet = StreamInlet(self.streams[stream_index])

        # Validate if serial_port is connected.
        ports = list(tools.list_ports.comports())

        if serial_port not in ports:
            raise ValueError("Serial Port not connected : %s" % serial_port)

        # Establish serial communication.
        self.serial_device = Serial(serial_port, baudrate=baud_rate)

        self.bci_data = []
        self.sensor_data = []
        self.has_finished = False
        
    # TODO -> Write the textfile with self.bci_data...
    def run_data_collection(self, samples):
        sensor_process = Process(target = get_sensor_samples, args = ())
        sensor_process.start()
        openbci_process = Process(target = get_openbci_samples, args = (samples,))
        openbci_process.start()
        sensor_process.join()
        openbci_process.join()


    def get_openbci_samples(self, samples):
        while samples > 0:
            bci_sample, timestamp = self.inlet.pull_sample()
            latest_sensor_data = self.get_latest_sensor_data(timestamp)
            self.bci_data.append([timestamp, bci_sample, latest_sensor_data])
            samples -= 1
        self.has_finished = True


    def get_sensor_samples(self):
        # Loop until the get_openbci_samples process finishes.
        while not self.has_finished:            
            # Get the latest sensor data.
            sensor_value = self.serial_device.readline().decode('ascii')
            sensor_timestamp = time()
            self.sensor_data.append([sensor_timestamp, sensor_value])

    def get_latest_sensor_data(self, timestamp):
        # Calculate the initial number of sensor samples.
        size = len(self.sensor_data)

        # Make sure there is data.
        if size == 0:
            raise ConnectionError("No sensor data at this point.")

        # Make sure the timestamp is greater or equal to the earliest sensor read.
        if timestamp < self.sensor_data[0][0]:
            raise ValueError("Invalid timestamp %s" % timestamp)        

        latest_data = self.sensor_data[size - 1]
        # If latest data corresponds to the given timestamp or only sensor read.
        if timestamp == latest_data[0]:
            return latest_data[1]

        # If the last value preceeds the timestamp, the sensor value remains the same.
        elif size == 1 or timestamp > latest_data[0]:
            self.sensor_data.append([timestamp, latest_data[1]])
            return latest_data[1]

        # Perform linear interpolation.
        else:
            data_index = size - 1
            # Find the data corresponding to the given timestamp 
            # or the one before the given timestamp.
            while data_index >= 0:
                latest_data = self.sensor_data[data_index]
                # Found value for the given timestamp.
                if latest_data[0] == timestamp:
                    return latest_data[1]
                
                elif latest_data[0] < timestamp:
                    break
                data_index -= 1
            x1 = latest_data[0]
            x2 = timestamp
            x3 = self.sensor_data[data_index + 1][0]
            y1 = latest_data[1]
            y3 = self.sensor_data[data_index + 1][1]
            return ((x2 - x1) * (y3 - y1))/ (x3 - x1) + y1

    #TODO -> Pass filename string 
    def write_to_csv(self, data_to_write):
        csv_file = open(self.filename, 'w', newline='')
        header = ['timestamp', 'sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5', 'sensor6', 'sensor7', 'sensor8', 'knee_angle']
        writer = DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for i in range(0, len(data_to_write)):
            writer.writerow({'timestamp': data_to_write[i][0],
            'sensor1': data_to_write[i][1][0],
            'sensor2':data_to_write[i][1][2],
            'sensor3':data_to_write[i][1][3],
            'sensor4':data_to_write[i][1][4],
            'sensor5':data_to_write[i][1][5],
            'sensor6':data_to_write[i][1][6],
            'sensor7':data_to_write[i][1][7],
            'sensor8':data_to_write[i][1][8],
            'knee_angle': data_to_write[i][2]})