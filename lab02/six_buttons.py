# more_video_control_cb.py
# 10/4/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# Checks if all six buttons work. Prints out which 
# GPIO button has been pressed.
#


import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(.1)
    i1 = GPIO.input(17)
    i2 = GPIO.input(22)
    i3 = GPIO.input(23)
    i4 = GPIO.input(27)
    i5 = GPIO.input(26)
    i6 = GPIO.input(19)
    if not i1:
        print("GPIO pin 17 pushed")
        quit()
    elif not i2:
        print("GPIO pin 22 pushed")
    
    elif not i3:
        print("GPIO pin 23 pushed")
    
    elif not i4:
        print("GPIO pin 27 pushed")
    elif not i5:
        print("GPIO pin 26 pushed")
    elif not i6:
        print("GPIO pin 19 pushed")








