#path setting
import sys
sys.path.insert(0, "/home/pi/remote_control_new/remote_control/remote_control")
from driver import camera, stream, wheels,esc_1060
#import picar
#picar.setup()

#initialization
db_file = "/home/pi/remote_control/remote_control/driver/config"

esc = esc_1060.ESC(1, 0x40,60, 10, 11)
#bw = wheels.Wheels(27, 4)
#fw = wheels.Wheels(17, 5)
##################################################################3######



#bw.ready()
#fw.ready()

SPEED = 100
#bw_status = 0
key = 0

#input command
esc.set_speed(3)
while key != 'q':
	key = raw_input("give command : ")
	print "input key : [" + key + "]"

	#move forward
	if key == "w":
		print "[forward]\n"
		#esc.set_speed(4)
		esc.forward()

		#bw.speed = SPEED
		#bw.clockwise()
		#bw_status = 1
		debug = "speed =", SPEED

	#move backward
	elif key == 's':
		print "[backward]\n"
		#esc.set_speed(1)
		esc.backward()
		#bw.speed = SPEED
		#bw.counterclockwise()

	#turn left
	elif key == 'a':
		print "[turn left]\n"
		esc.left()
		#fw.speed = 100
		#fw.clockwise()

	#turn right
	elif key == 'd':
		print "[turn right]\n"
		esc.right()
		#fw.speed = 100
		#fw.counterclockwise()

	#exit
	elif key == 'q':
		print "[stop] entered\n"
		esc.stop()
		#fw.stop()
		#bw.stop()
		#bw_status = 0
		sys.exit()

	#wrong input
	else :
		print "Wrong Input Command\n"
