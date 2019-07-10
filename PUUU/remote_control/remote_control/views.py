'''
**********************************************************************
* Filename    : viewsws
* Description : views for server
* Author      : Sangyun.Kwon
* Brand       : MagicEco
* Website     : www.magice.co
* Update      : Sangyun.Kwon    2019-03-24    New release
**********************************************************************
'''

from django.shortcuts import render_to_response
#from driver import stream
from django.http import HttpResponse
import os
from remote_control.driver import camera, esc_1060, stream


db_file = "/home/pi/remote_control_new/remote_control/remote_control/driver/config"
esc = esc_1060.ESC(1, 0x40, 60, 10, 11)

cam = camera.Camera(debug=False, db=db_file, address = 0x60)
SPEED = 60

print stream.start()

def home(request):
    return render_to_response("base.html")

def run(request):

    global SPEED, bw_status
    debug = ''

    if 'action' in request.GET:
        action = request.GET['action']
    # ============== Back wheels =============
        if action == 'bwready':

            esc.stop()
        elif action == 'forward':

            esc.forward()
            debug = "speed =", SPEED
        elif action == 'backward':
            #bw.speed = SPEED
            #bw.counterclockwise()
            #bw_status = -1
            esc.backward()
        elif action == 'stop':
            esc.stop()
    # ============== Front wheels =============
        elif action == 'fwready':
            esc.set_speed(2)
            esc.center()
        elif action == 'fwleft':
            esc.left()
        elif action == 'fwright':
            esc.right()
        elif action == 'fwstraight':
            esc.center()
            
            
        elif 'fwturn' in action:
            print "turn %s" % action
        # ================ Camera =================
        elif action == 'camready':
            cam.ready()
            print "camready"
        elif action == "camleft":
            cam.turn_left(40)
            print "camleft"
        elif action == 'camright':
            cam.turn_right(40)
            print "camright"
        elif action == 'camup':
            cam.turn_up(20)
            print "camup"
        elif action == 'camdown':
            print "camdown"
            cam.turn_down(20)

    if 'speed' in request.GET:
        speed = int(request.GET['speed'])
        SPEED = speed
        if speed < 0:
            speed = 0
        if speed > 100:
            speed = 100
            SPEED = speed
        speed /= 12
        esc.set_speed(speed)
        
    host = stream.get_host().split(' ')[0]
    return render_to_response("run.html", {'host': host})

def connection_test(request):
	return HttpResponse('OK')
