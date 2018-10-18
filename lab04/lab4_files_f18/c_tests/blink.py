# blink.py
# 10/18/18 
# Lab 03
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# blinks LED and exits if 'q' is pressed. Otherwise waits for command
# 
# 
import RPi.GPIO as GPIO
import time
import sys


frequency = sys.argv[1]
print frequency
dc = 50

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.OUT)
p = GPIO.PWM(13,float( frequency))
 
p.start(dc) # where dc is the duty cycle (0.0 <= dc <= 100.0)

time.sleep(60)

GPIO.cleanup()
