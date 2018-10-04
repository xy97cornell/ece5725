# more_video_control.py
# 10/4/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
# Lab 02
#
# Controls the video with two extra buttons 
# Uses polling to check for commands
# Adds fast forward 30 seconds and rewind 30 seconds functionality
#


import time
import RPi.GPIO as GPIO
import subprocess
import threading


GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO for external button
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO for external button

while True:
    i1 = GPIO.input(17)
    i2 = GPIO.input(22)
    i3 = GPIO.input(23)
    i4 = GPIO.input(27)
    i5 = GPIO.input(26)
    i6 = GPIO.input(19)
    # poll for button presses 
    if i1 == 0:
        subprocess.call('echo "pause" > video_fifo', shell=True)
        time.sleep(0.2)
    elif i2 == 0:
        subprocess.call('echo "seek 10 0" > video_fifo', shell=True)
   
        time.sleep(0.2)
    elif i3 == 0:
        subprocess.call('echo "seek -10 0" > video_fifo', shell=True)
        time.sleep(0.2)
   
    elif i4 == 0:
        subprocess.call('echo "quit" > video_fifo', shell=True)
        time.sleep(0.2)
        quit()
   
    elif i5 == 0:
        subprocess.call('echo "seek" 30 0 > video_fifo', shell=True)
        time.sleep(0.2)

    elif i6 == 0:
        subprocess.call('echo "seek" -30 0 > video_fifo', shell=True)
        time.sleep(0.2)

