# This code was adapted from the following URL:
#   https://stackoverflow.com/questions/2291772/virtual-serial-device-in-python

import os
import pty
import serial
import time

master, slave = pty.openpty()
s_name = os.ttyname(slave)
ser = serial.Serial(s_name)

while True:

    # Publish data into serial stream (SERVER).
    ser.write(str.encode("90"))

    # Fetch data from serial stream (CLIENT).
    data = os.read(master, 1000)

    # Use data on client side.
    print(data)

    # Wait before publishing/consuming next data (T=2ms).
    time.sleep(0.02)
