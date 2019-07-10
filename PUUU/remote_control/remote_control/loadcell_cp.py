#from pyfirmata import Arduino. util
#import time
import sys
sys.path.insert(0,"/home/pi/remote_control_new/remote_control/remote_control")
from driver import camera,stream,wheels,esc_1060
db_file = "/home/pi/remote_control/remote_control/driver/config"
esc = esc_1060.ESC(1,0x40,60,10,11)

SPEED =100

key =0 

esc.set_speed(3)

import serial
port = "/dev/ttyACM0"

#pin_button = board.get_pin('d:8:i')


#it= util.Iterator(board)
#it.start()
#pin_button.enable_reporting()
serialFromArduino = serial.Serial(port,115200)
serialFromArduino.flushInput()
#esc.forward()
#debug="speed = ",SPEED
while True:
    input_s = serialFromArduino.readline()
    print(input_s[10])
    #input = int(input_s)
    """if int(input_s[1])>=5 :
        esc.backward()
    elif int(input_s[1])<5:
        esc.stop()
"""
    debug = "speed = ",SPEED
#    esc.backward()
#    debug = "speed = ",SPEED
    print(input_s)


#esc.stop()
#sys.exit()
