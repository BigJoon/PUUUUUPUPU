from pca9685 import PWM
import time

pwm = PWM()
pwm.frequency = 60
pwm.setup()

class ESC(object):
    '''
    This class is made to use ESC device in Raspberry Pi.
    Becareful when you connect ESC to your Raspberry Pi board.
    It need very large current, it can make broken your circuit.

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
        self.drive_NEUTRAL = 390 #default value. It needs to calibrate
        self.drive_MIN = 0
        self.drive_MAX = 500
        self.steer_val = self.steer_NEUTRAL
        self.drive_val = self.drive_NEUTRAL
        self.speed_forward = self.steer_NEUTRAL
        self.speed_backward = self.steer_NEUTRAL
        self.steer_diff = 25
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
        
        self.pwm.write(self.drive, 0, self.speed_forward)

    def decrease_speed(self):
        if self.speed_forward > self.drive_NEUTRAL:
            self.speed_forward -= self.drive_diff
            if self.speed_forward < self.drive_NEUTRAL:
                self.speed_forward = self.drive_NEUTRAL
        
        if self.speed_backward < self.drive_NEUTRAL:
            self.speed_backward += self.drive_diff
            if self.speed_backward > self.drive_NEUTRAL :
                self.speed_backward = self.drive_NEUTRAL

        self.pwm.write(self.drive, 0, self.speed_forward)
        
    def set_speed(self, speed_val = 1):
        '''
        speed_val : it should set number between 1 to 12
        '''
        if speed_val > 12:
            speed_val = 12
        self.speed_forward = self.drive_NEUTRAL + self.drive_diff*speed_val
        self.speed_backward = self.drive_NEUTRAL - self.drive_diff*speed_val
        print "set_speed === fwd : ", self.speed_forward, "bwd : ", self.speed_backward
    
    def set_calib_speed(self, speed_val = 1300):
        self.speed_forward = speed_val

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
    esc = ESC()
    #esc calibration sequence
    esc.set_calib_speed(0)
    esc.forward()
    time.sleep(2)
    '''
    esc.set_calib_speed(240)
    esc.forward()
    time.sleep(2)
    
    esc.set_calib_speed(500)
    esc.forward()
    time.sleep(2)
    '''
    
    esc.set_calib_speed(370)
    esc.forward()
    time.sleep(1)
    
    esc.set_calib_speed(240)
    esc.forward()
    time.sleep(1)

    esc.set_calib_speed(370)
    esc.forward()
    time.sleep(1)

    esc.set_calib_speed(240)
    esc.forward()
    time.sleep(1)

    esc.set_calib_speed(0)
    esc.forward()
    time.sleep(1)
    
    '''
    esc.set_calib_speed(1390)
    esc.forward()
    time.sleep(1)
    esc.set_calib_speed(1750)
    esc.forward()
    time.sleep(1)
    '''
    
    '''
    esc.set_calib_speed(1570)
    esc.forward()
    '''
    
    while True:
        value = input("Input calibration value : ")
        
        if value < 0 or value > 4096:
            print "Input value was wrong \n"
        else :
            esc.set_calib_speed(value)
            esc.forward()
