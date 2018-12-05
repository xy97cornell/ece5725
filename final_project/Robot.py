import RPi.GPIO as GPIO 
import time


IDLE = 0
START = 1

class Robot:
	
	
    LEFT_SERVO_PIN = 6
    RIGHT_SERVO_PIN = 13
    STOP_T  = 0.0015 
    CLKW_T  = 0.0013
    CCLKW_T = 0.0017
    DOWN_T  = 0.02
    STOP_DC = STOP_T/(STOP_T+DOWN_T)*100 #cycle in percentage
    STOP_FREQ = 1/(STOP_T+DOWN_T)
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LEFT_SERVO_PIN, GPIO.OUT)
        GPIO.setup(self.RIGHT_SERVO_PIN, GPIO.OUT)
        #self.left_servo_freq = STOP_FREQ
        #self.right_servo_freq = STOP_FREQ
        #self.left_servo_dc = STOP_DC
        #self.left_servo_dc = self.STOP_DC

        #self.left_servo = GPIO.PWM(self.LEFT_SERVO_PIN, self.left_servo_freq)
        #self.right_servo = GPIO.PWM(self.RIGHT_SERVO_PIN, self.right_servo_freq)
        self.left_servo = GPIO.PWM(self.LEFT_SERVO_PIN, self.STOP_FREQ)
        self.right_servo = GPIO.PWM(self.RIGHT_SERVO_PIN, self.STOP_FREQ)
        self.state = IDLE

    def stop(self):
        self.left_servo.ChangeDutyCycle(self.STOP_DC)
        self.right_servo.ChangeDutyCycle(self.STOP_DC)
        self.left_servo.ChangeFrequency(self.STOP_FREQ)
        self.right_servo.ChangeFrequency(self.STOP_FREQ)
    


    def forward(self):
        print("Moving forward")
        self.left_servo.ChangeDutyCycle(self.CCLKW_T/(self.CCLKW_T+self.DOWN_T)*100)
        self.left_servo.ChangeFrequency(1/(self.CCLKW_T+self.DOWN_T))
        self.right_servo.ChangeDutyCycle(self.CLKW_T/(self.CLKW_T+self.DOWN_T)*100)
        self.right_servo.ChangeFrequency(1/(self.CLKW_T+self.DOWN_T))

    def left(self):
        print("Moving left")
        self.left_servo.ChangeDutyCycle(self.CLKW_T/(self.CLKW_T+self.DOWN_T)*100)
        self.left_servo.ChangeFrequency(1/(self.CLKW_T+self.DOWN_T))
        self.right_servo.ChangeDutyCycle(self.CLKW_T/(self.CLKW_T+self.DOWN_T)*100)
        self.right_servo.ChangeFrequency(1/(self.CLKW_T+self.DOWN_T))
    
    def right(self):
        print("Moving right")
        self.left_servo.ChangeDutyCycle(self.CCLKW_T/(self.CCLKW_T+self.DOWN_T)*100)
        self.left_servo.ChangeFrequency(1/(self.CCLKW_T+self.DOWN_T))
        self.right_servo.ChangeDutyCycle(self.CCLKW_T/(self.CCLKW_T+self.DOWN_T)*100)
        self.right_servo.ChangeFrequency(1/(self.CCLKW_T+self.DOWN_T))

    

    def command(self, input_str):
        '''
        Values_List = 
        [forward, forward_magnitude, right, right_magnitude, left, left_magnitude, stop] 
        '''
        value_list = input_str.split(':')
        stop = int(value_list[6])
        forward = int(value_list[0])
        forward_magnitude = int(value_list[1])
        right = 


    def calibrate(self):
        self.left_servo.start(self.STOP_DC)
        self.right_servo.start(self.STOP_DC)
        self.stop()
        time.sleep(5)
        self.forward()
        time.sleep(5)
        self.right()
        time.sleep(5)
        self.left()
        time.sleep(5)
	
    
    def shutdown(self):
        GPIO.cleanup()
	

    def exit(self):
        GPIO.cleanup()
	


'''def set_speed(interval1, interval2):
    p1.ChangeDutyCycle(interval1/(2000.0+interval1)*100)
    p1.ChangeFrequency(100000/(2000.0+interval1))
    p2.ChangeDutyCycle(interval2/(2000.0+interval2)*100)
    p2.ChangeFrequency(100000/(2000.0+interval2))
'''


if __name__=='__main__':
	
	robot = Robot()
	robot.calibrate()
	robot.shutdown()
