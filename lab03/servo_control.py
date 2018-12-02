# servo_control.py
# 10/18/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
# Lab 03
#
# Steps through the servo rotation speeds and 
# directions in a step increment. We turn from 
# stopped position to full clockwise rotation
# to full counterclockwise rotation.
#


import RPi.GPIO as GPIO
import time
import sys 

#frequency = 50
dc = 7.5
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.OUT)
code_running = True
 
def GPIO17_callback(channel):
    global code_running
    code_running = False
p = GPIO.PWM(6, 10)
GPIO.add_event_detect(17, GPIO.FALLING, \
callback=GPIO17_callback, bouncetime=300)

# where dc is the duty cycle (0.0 <= dc <= 100.0)

p.start(dc) 

while code_running:
    try:
        for h in range(150, 129, -2):
            #print dc/100.0
            frequency = 100000/(h + 2000.0)
            p.ChangeFrequency(frequency)
            dc = h/(h+2000.0)*100
            p.ChangeDutyCycle(dc)
            print(dc, frequency)
            time.sleep(100)
        for h in range(150, 171, 2): 
            frequency = 100000/(h + 2000.0)
            p.ChangeFrequency(frequency)
            dc = h/(h+2000.0) *100
            p.ChangeDutyCycle(dc)
            print(dc, frequency)
            time.sleep(100)
        code_running = False
    except KeyboardInterrupt:
        code_running = False

p.stop()
GPIO.cleanup()
