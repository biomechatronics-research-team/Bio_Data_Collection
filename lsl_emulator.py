# This code is adapted from the following repository:
#   https://github.com/chkothe/pylsl/blob/master/examples/SendData.py

import random
import time
from pylsl import StreamInfo, StreamOutlet

# Initialize an LSL stream by providing the stream-name ('BioSemi'),
# signal type ('EEG'), number of channels (8 for the OpenBCI Mark IV headset),
# sampling frequency (250 for the OpenBCI Mark IV headset), the data type ('float32'),
# and the user-id.
info = StreamInfo('BioSemi', 'EEG', 8, 250, 'float32', 'myuid34234')

# Create a server outlet.
outlet = StreamOutlet(info)

while True:

    # Create random 8-channel sample.
    mysample = [random.random(), random.random(), random.random(),
                random.random(), random.random(), random.random(),
                random.random(), random.random()]

    # Send the signal and wait 4ms for the next data post (emulating 250 Hz sampling rate).
    outlet.push_sample(mysample)
    time.sleep(0.04)
