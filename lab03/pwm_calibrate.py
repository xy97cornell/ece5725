# pwm_calibrate.py
# 10/18/18 
# Lab 03
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# Calibrates the servos by sending the servo to the expected
# stop PWM signal. This allows us to odjust potentiometer in 
# the servo to calibrate it.  
# 


import RPi.GPIO as GPIO
import time
import sys 

#GPIO.cleanup()
frequency = 1000/(1.5 + 20.0)
dc = 1.5/(1.5 + 20.0)*100
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.OUT) #GPIO 13 as PWM output for servo
GPIO.setup(6, GPIO.OUT)
p0 = GPIO.PWM(13, frequency)
p1 = GPIO.PWM(6, frequency)

def GPIO17_callback(channel):
    """Exit interrupt button"""
    GPIO.cleanup()
    sys.exit(1)

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
p0.start(dc) 
p1.start(dc)

time.sleep(15)

GPIO.cleanup()
