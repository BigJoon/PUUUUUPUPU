#!/usr/bin/env python
'''
**********************************************************************
* Filename    : wheels.py
* Description : A module to control a motor wheels of RPi Car
* Author      : syun.kwon
* Brand       : MagicEco
* E-mail      :
* Website     : www.magice.co
* Update      : syun.kwon    2019-01-16    New release
*
**********************************************************************
'''

import TB6612
import PCA9685
#import filedb

class Wheels(object):
    ''' Wheels control class '''

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "wheels.py":'

    def __init__(self, val_GPIO=0, val_PWM=0, debug=False, bus_number=1, db="config"):
        ''' Init the direction channel and pwm channel '''
        ''' val_GPIO and val_PWM is very important to motor driving'''
        self.MOTOR_GPIO = val_GPIO
        self.PWM_SOURCE = val_PWM

        self.motor_direction = False
        self.selected_motor = TB6612.Motor(self.MOTOR_GPIO, offset=self.motor_direction)

        self.pwm_source = PCA9685.PWM(bus_number=bus_number)
        self.pwm_source.setup()
        self.pwm_source.frequency = 60

        def _set_pwm(value):
            pulse_wide = self.pwm_source.map(value, 0, 100, 0, 4095)
            self.pwm_source.write(self.PWM_SOURCE, 0, pulse_wide)

        self.selected_motor.pwm = _set_pwm

        self._speed = 0

        self.debug = debug
        if self._DEBUG:
            print self._DEBUG_INFO, 'Set right wheel to #%d, PWM channel to %d' % (self.MOTOR_GPIO, self.PWM_SOURCE)

    def clockwise(self):
        ''' Move both wheels forward '''
        '''self.steer_motor.forward()'''
        self.selected_motor.forward()
        if self._DEBUG:
            print self._DEBUG_INFO, 'Running Clockwise'

    def counterclockwise(self):
        ''' wheels backward '''
        '''self.steer_motor.backward()'''
        self.selected_motor.backward()
        if self._DEBUG:
            print self._DEBUG_INFO, 'Running Counter clockwise'

    def stop(self):
        ''' Stop both wheels '''
        #self.steer_motor.stop()
        self.selected_motor.stop()
        if self._DEBUG:
            print self._DEBUG_INFO, 'Stop'

    @property
    def speed(self, speed):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed
        ''' Set moving speeds '''
        #self.steer_motor.speed = self._speed
        self.selected_motor.speed = self._speed
        if self._DEBUG:
            print self._DEBUG_INFO, 'Set speed to', self._speed

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        ''' Set if debug information shows '''
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            print self._DEBUG_INFO, "Set debug on"
            self.selected_motor.debug = True
            self.pwm_source.debug = True
        else:
            print self._DEBUG_INFO, "Set debug off"
            self.selected_motor.debug = False
            self.pwm_source.debug = False

    def ready(self):
        ''' Get the back wheels to the ready position. (stop) '''
        if self._DEBUG:
            print self._DEBUG_INFO, 'Turn to "Ready" position'
        self.selected_motor.offset = self.motor_direction
        self.stop()

def test():
    import time
    drive_wheels = Wheels(27, 4)
    drive_wheels.ready()
    steer_wheels = Wheels(17,5)
    drive_wheels.ready()
    DELAY = 0.01
    try:
        drive_wheels.clockwise()
        for i in range(0, 100):
            drive_wheels.speed = i
            print "FWD, speed =", i
            time.sleep(DELAY)
        for i in range(100, 0, -1):
            drive_wheels.speed = i
            print "FWD, speed =", i
            time.sleep(DELAY)

        drive_wheels.counterclockwise()
        for i in range(0, 100):
            drive_wheels.speed = i
            print "BWD, speed =", i
            time.sleep(DELAY)
        for i in range(100, 0, -1):
            drive_wheels.speed = i
            print "BWD, speed =", i
            time.sleep(DELAY)

        steer_wheels.clockwise()
        for i in range(0, 100):
            steer_wheels.speed = i
            print "LEFT, speed =", i
            time.sleep(DELAY)
        for i in range(100, 0, -1):
            steer_wheels.speed = i
            print "LEFT, speed =", i
            time.sleep(DELAY)

        steer_wheels.counterclockwise()
        for i in range(0, 100):
            steer_wheels.speed = i
            print "RIGHT, speed =", i
            time.sleep(DELAY)
        for i in range(100, 0, -1):
            steer_wheels.speed = i
            print "RIGHT, speed =", i
            time.sleep(DELAY)

    except KeyboardInterrupt:
        print "KeyboardInterrupt, motor stop"
        drive_wheels.stop()
        steer_wheels.stop()
    finally:
        print "Finished, motor stop"
        drive_wheels.stop()
        steer_wheels.stop()

if __name__ == '__main__':
    test()
