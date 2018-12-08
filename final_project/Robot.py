# Robot.py
# 12/7/2018 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
# Final Project - Telepresence Vehicle
#
# Robot class for controling the robot by setting the timings for
# the GPIO pins. We also decode control messages from the basestation. 
# 


import RPi.GPIO as GPIO 
import time

class Robot:
    """
    Initializes the two servos using RPi.GPIO library to control GPIO. 
    Handles the timing of the servos and sets the speed and rotation 
    directions of the robot
    """
	
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
        self.right_speed = self.STOP_T
        self.left_speed  = self.STOP_T
        self.left_servo = GPIO.PWM(self.LEFT_SERVO_PIN, self.STOP_FREQ)
        self.right_servo = GPIO.PWM(self.RIGHT_SERVO_PIN, self.STOP_FREQ)
        self.left_servo.start(self.STOP_DC)
        self.right_servo.start(self.STOP_DC)

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
        print(str(interval1) + ' ' + str(interval2))
        if interval1 !=-1:
            self.left_servo.ChangeDutyCycle(interval1/(self.DOWN_T+interval1)*100)
            self.left_servo.ChangeFrequency(1/(self.DOWN_T+interval1))
        if interval1 != -1:
            self.right_servo.ChangeDutyCycle(interval2/(self.DOWN_T+interval2)*100)
            self.right_servo.ChangeFrequency(1/(self.DOWN_T+interval2))
	
    def command(self, input_str):
        '''
        Decodes message from the base station
        Values_List = [Valid,turn,heading,roll,pitch] 
        Parameter input_str: string of commands sent through UDP
        Moves robot if turn is 1
        Stops robot if turn or valid is 0
        Decodes the robot speed and direction based on heading and
        pitch
        '''
        data = input_str.split(':')
        valid = int(data[0])
        if valid: 
            turn = int(data[1])
            if turn:
                h = float(data[2])
                r = float(data[3])
                p = float(data[4])
                
                if r>180:
                    r-=360
                elif r<-180:
                    r+=360
                if p>180:
                    p-=360
                elif p<-180:
                    p+=360
                
                threshold = 5
                
                if r<threshold and r>-threshold:
                    r = 0
                if p<threshold and p>-threshold:
                    p = 0
                
                roll_max = 50
                roll_min = -50
                pitch_max = 50
                pitch_min = -50
                if r<roll_min:
                    roll = roll_min
                elif r>roll_max:
                    roll = roll_max
                else:
                    roll = r
                if p<pitch_min:
                    pitch = pitch_min
                elif p>pitch_max:
                    pitch = pitch_max
                else:
                    pitch = p
                
                rslope = 0.0001/roll_max
                pslope = 2*rslope
                
                left = self.left_speed + rslope*roll - pslope * pitch
                right = self.right_speed + rslope*roll + pslope * pitch 
                
                if left>self.CCLKW_T:
                    left = self.CCLKW_T
                if right<self.CLKW_T:
                    right = self.CLKW_T
                
                self.set_speed(left,right)
                print ("left: "+str(left)+" right:"+str(right))
            else:
                self.stop()
			
        else:
            self.stop()


    def calibrate(self):
        """
        Calibrates the servo by setting the robot to move in all
        four directions
        """
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


if __name__=='__main__':
	
	robot = Robot()
	
	
	robot.calibrate()
	robot.shutdown()
