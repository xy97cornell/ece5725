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
frequency = 0.5 
dc = 50

GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.OUT)
p = GPIO.PWM(5, frequency)
code_running = True
 
p.start(dc) # where dc is the duty cycle (0.0 <= dc <= 100.0)

while (code_running):
    a = raw_input("select freq")
    if(a=='q'):
        code_running = False
    else: 
        try:
            a = int(a)
            p.ChangeFrequency(a) # where freq is the new frequency in Hz
        except ValueError:
            pass
        


GPIO.cleanup()
