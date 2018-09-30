# more_video_control_cb.py
# 10/4/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# Controls the video with two extra buttons 
# Uses GPIO interrupts to check for commands
# Adds fast forward 30 seconds and rewind 30 seconds functionality
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


def GPIO17_callback(channel):
    """
    interrupt handler for GPIO17; button on piTFT
    """
    print "in interrupt 17"
    subprocess.call('echo "pause" > video_fifo', shell=True)


def GPIO22_callback(channel):
    """
    interrupt handler for GPIO22; button on piTFT
    """
    print "in interrupt 22"
    subprocess.call('echo "seek 10 0" > video_fifo', shell=True)


def GPIO23_callback(channel):
    """
    interrupt handler for GPIO23; button on piTFT
    """
    print "in interrupt 23"
    subprocess.call('echo "seek -10 0" > video_fifo', shell=True)


def GPIO27_callback(channel):
    """
    interrupt handler for GPIO27; button on piTFT
    """
    print "in interrupt 27"
    subprocess.call('echo "quit" > video_fifo', shell=True)

def GPIO26_callback(channel):
    """
    interrupt handler for GPIO26; external button
    """
    print "in interrupt 26"
    subprocess.call('echo "seek" 30 0 > video_fifo', shell=True)


def GPIO19_callback(channel):
    """
    interrupt handler for GPIO19; external button
    """
    print "in interrupt 19"
    subprocess.call('echo "seek" -30 0 > video_fifo', shell=True)
    
# Setup the GPIO pins as interrupts
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, callback=GPIO19_callback, bouncetime=300)

try:
    GPIO.wait_for_edge(27, GPIO.FALLING) #wait for exit putton to be pressed
except KeyboardInterrupt:
    GPIO.cleanup() #cleans the GPIO in case of usage of CTRL C
    print "keyboardInterrupt"

#If exit button pressed. Exit video and terminate code
subprocess.call('echo "quit" > video_fifo', shell=True)
GPIO.cleanup()    
