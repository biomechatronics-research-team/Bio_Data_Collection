


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
            self.channels = channels_data
            self.timestamp = timestamp



    # Defining data collection methods.

    # TODO -> Implement data collection method only considering data from the headset.
    def collect_mark4lsl(self, num_samples, lsl_name):
        return 0

    # TODO -> Implement data collection method considering data from headset & knee angle.
    def collect_mark4lsl_kneeserial(self, num_samples, lsl_name, serial_name, baud_rate):
        return 0

    
# Make sure Serial & LSL mock streams are running before running this file.
if __name__ == '__main__':

    # Prepairing Mock Test.
    num_samples = 20
    lsl_name = "cool_stream"
    serial_name = "cool_serial"
    baud_rate = 9600

    # Initializing mock BioStream.
    mock = BioStream()

    # Mock testing the data collection methods.
    data_mark4 = mock.collect_mark4lsl(num_samples, lsl_name)
    data_mark4_knee = mock.collect_mark4lsl_kneeserial(num_samples, lsl_name, serial_name, baud_rate)

    # Displaying Mark4 results.
    print("Mark4:", data_mark4)

    # Displaying Mark4 + Knee Angle results.
    print("Mark4 + Knee Angle:", data_mark4_knee)