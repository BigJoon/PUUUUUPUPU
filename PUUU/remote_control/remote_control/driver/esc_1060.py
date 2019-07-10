from PCA9685 import PWM
import time

class ESC(object):
    '''
    This class is made to use ESC device in Raspberry Pi.
    Becareful when you connect ESC to your Raspberry Pi board.
    It needs very large current, it can make broken your circuit.

    '''
    def __init__(self, bus_number=None, address=0x40, frequency = 60, drive = 0, steer = 1):
        ''' This is very important part of set ESC.
        If you want to drive motor by this source, you have to use pca9685 drive.
        Because the ESC circuit is connected with PCA9685 PWM circuit board's channel pins

        Argument
        bus_number : bus type of raspberry Pi. If it doesn't set, pca9685 module set value as default.
        address : I2C slave address
        frequency : driving motor(forward/backward motor) PWM frequency.
        driver : pca9685 channel number of driving motor
        steer : pca9685 channel number of steering motor
        '''
        self.pwm = PWM(bus_number, address)
        self.pwm.frequency = frequency
        self.pwm.setup()
        self.drive = drive
        self.steer = steer
        self.steer_NEUTRAL = 390 #default value. It needs to calibrate
        self.steer_MIN = 280
        self.steer_MAX = 500
        self.drive_NEUTRAL = 389 #default value. It needs to calibrate
        self.drive_MIN = 280
        self.drive_MAX = 450
        self.steer_val = self.steer_NEUTRAL
        self.drive_val = self.drive_NEUTRAL
        self.speed_forward = self.steer_NEUTRAL
        self.speed_backward = self.steer_NEUTRAL
        self.steer_diff = 35
        self.drive_diff = 5
        self.is_stop = True

    def calibrate_drive_NEUTRAL(self, cal_value = 390):
        if cal_value > self.drive_MAX or cal_value < self.drive_MIN:
            print "Calibration value Fail"
        else:
            self.drive_NEUTRAL = cal_value

    def calibrate_steer_NEUTRAL(self, cal_value = 390):
        if cal_value > self.steer_MAX or cal_value < self.steer_MIN:
            print "Stree Calibration value Fail"
        else:
            self.steer_NEUTRAL = cal_value

    def set_steer_strength(self, strength = 35):
        if strength > (self.steer_MAX - self.steer_NEUTRAL):
            strength = self.steer_MAX - self.steer_NEUTRAL
        elif strength < (self.steer_NEUTRAL - self.steer_NEUTRAL):
            strength = self.steer_NEUTRAL - self.steer_NEUTRAL
        self.steer_diff = strength

    def left(self):
        if self.steer_val < self.steer_MAX:
            self.steer_val += self.steer_diff
            if self.steer_val > self.steer_MAX:
                self.steer_val = self.steer_MAX

        self.pwm.write(self.steer,0,self.steer_val)
        
    def right(self):
        if self.steer_val > self.steer_MIN:
            self.steer_val -= self.steer_diff
            if self.steer_val < self.steer_MIN :
                self.steer_val = self.steer_MIN
        self.pwm.write(self.steer,0,self.steer_val)
    
    def center(self):
        self.steer_val = self.steer_NEUTRAL
        self.pwm.write(self.steer,0,self.steer_val)
        time.sleep(0.1)
        self.pwm.write(self.steer,0,0)

    def increase_speed(self):
        if self.speed_forward < self.drive_MAX:
            self.speed_forward += self.drive_diff
            if self.speed_forward > self.drive_MAX:
                self.speed_forward = self.drive_MAX
        
        if self.speed_backward > self.drive_MIN:
            self.speed_backward -= self.drive_diff
            if self.speed_backward < self.drive_MIN :
                self.speed_backward = self.drive_MIN
        print "set_speed === fwd : ", self.speed_forward, "bwd : ", self.speed_backward

    def decrease_speed(self):
        if self.speed_forward > self.drive_NEUTRAL:
            self.speed_forward -= self.drive_diff
            if self.speed_forward < self.drive_NEUTRAL:
                self.speed_forward = self.drive_NEUTRAL
        
        if self.speed_backward < self.drive_NEUTRAL:
            self.speed_backward += self.drive_diff
            if self.speed_backward > self.drive_NEUTRAL :
                self.speed_backward = self.drive_NEUTRAL
        print "set_speed === fwd : ", self.speed_forward, "bwd : ", self.speed_backward

    def set_speed(self, speed_val = 1):
        '''
        speed_val : it should set number between 1 to 12
        '''
        if speed_val > 12:
            speed_val = 12
        self.speed_forward = self.drive_NEUTRAL + self.drive_diff*speed_val
        self.speed_backward = self.drive_NEUTRAL - self.drive_diff*speed_val
        print "set_speed === fwd : ", self.speed_forward, "bwd : ", self.speed_backward

    def forward(self):
        if self.is_stop:
            self.pwm.write(self.drive, 0, self.steer_NEUTRAL)
            time.sleep(0.1)
            self.is_stop = False
        self.pwm.write(self.drive, 0, self.speed_forward)
    
    def backward(self):
        if self.is_stop:
            self.pwm.write(self.drive, 0, self.steer_NEUTRAL)
            time.sleep(0.1)
            self.is_stop = False
        self.pwm.write(self.drive, 0,self.speed_backward)

    def stop(self):
        self.pwm.write(self.drive, 0,0)
        self.is_stop = True

if __name__ == '__main__':
    import curses

    screen = curses.initscr()
    #curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    esc = ESC(1, 0x40, 60, 10,11)

    while True:
            char = screen.getch()
            if char == ord('q'):
                    break
            else:
                    if char == curses.KEY_UP:
                        esc.forward()
                    elif char == curses.KEY_DOWN:
                        esc.backward()
                    elif char== curses.KEY_RIGHT:
                        esc.right()
                    elif char == curses.KEY_LEFT:
                        esc.left()
                    elif char == ord(' '):
                        esc.stop()
                        esc.center()
                    elif char == ord('['):
                        esc.increase_speed()
                    elif char == ord(']'):
                        esc.decrease_speed()
                    elif char == ord('1'):
                        esc.set_speed(1)
                    elif char == ord('2'):
                        esc.set_speed(2)
                    elif char == ord('3'):
                        esc.set_speed(3)
                    elif char == ord('4'):
                        esc.set_speed(4)
                    elif char == ord('5'):
                        esc.set_speed(5)
            
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
