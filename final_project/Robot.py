import RPi.GPIO as GPIO 
import time



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

	
	
	def calibrate(self):
		self.left_servo.start(self.STOP_DC)
		self.right_servo.start(self.STOP_DC)
		time.sleep(100)
	
	def shutdown(self):
		GPIO.cleanup()
	
	def exit(self):
		GPIO.cleanup()
	


'''def set_speed(interval1, interval2):
    p1.ChangeDutyCycle(interval1/(2000.0+interval1)*100)
    p1.ChangeFrequency(100000/(2000.0+interval1))
    p2.ChangeDutyCycle(interval2/(2000.0+interval2)*100)
    p2.ChangeFrequency(100000/(2000.0+interval2))'''


if __name__=='__main__':
	
	robot = Robot()
	robot.calibrate()
	robot.shutdown()
