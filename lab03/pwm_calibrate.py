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


frequency = 100000/(150 + 2000.0)
dc = 150/(150 + 2000.0)*100
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.OUT) #GPIO 13 as PWM output for servo
p = GPIO.PWM(13, frequency)
 
def GPIO17_callback(channel):
    """Exit interrupt button"""
    GPIO.cleanup()
    sys.exit(1)

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
p.start(dc) 
time.sleep(10)
    
GPIO.cleanup()
