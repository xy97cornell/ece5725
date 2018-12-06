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

    def set_speed(self, interval1, interval2):
		self.left_servo.ChangeDutyCycle(interval1/(2000.0+interval1)*100)
		self.left_servo.ChangeFrequency(100000/(2000.0+interval1))
		self.right_servo.ChangeDutyCycle(interval2/(2000.0+interval2)*100)
		self.right_servo.ChangeFrequency(100000/(2000.0+interval2))
	
    def command(self, input_str):
        '''
        Values_List = 
        [heading,roll,pitch] 
        '''
        data = input_str.split(':')
        h = data[0]
        r = data[1]
        p = data[2]
        threshold = 3
        roll_max = 35
        roll_min = -35
        direction = 0 #forward
        if r<-roll_min:
			turn = -30
		elif r>roll_max:
			turn = 30
		else:
			turn = r
		
		if r<threshold:
			direction = 1 #right
		elif r>threshold:
			direction = 2 #left
			
		slopeCW = 1.0*((self.CCLKW_T-self.STOP_T)/(row_max-threshold))
		slopeCCW  = 1.0*((self.CLKW_T-self.STOP_T)/(-1*(row_min-threshold)))
		output = 
        


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
	



if __name__=='__main__':
	
	robot = Robot()
	
	
	#robot.calibrate()
	robot.shutdown()
