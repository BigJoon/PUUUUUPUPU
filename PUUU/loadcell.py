#from pyfirmata import Arduino. util
#import time

import serial
port = "/dev/ttyACM0"

#pin_button = board.get_pin('d:8:i')


#it= util.Iterator(board)
#it.start()
#pin_button.enable_reporting()
serialFromArduino = serial.Serial(port,115200)
serialFromArduino.flushInput()

while True:
    input_s = serialFromArduino.readline()
    #input = int(input_s)
    print(input_s)
