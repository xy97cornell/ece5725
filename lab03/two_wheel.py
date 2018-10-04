# more_video_control_cb.py
# 10/4/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
# Lab 02
#
# Controls the video with two extra buttons 
# Uses GPIO interrupts to check for commands
# Adds fast forward 30 seconds and rewind 30 seconds functionality
#

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)


dc1 = 150/2150.0*100
dc2 = 150/2150.0*100
f1 = 100000/2150.0
f2 = 100000/2150.0
p1 = GPIO.PWM(6, f1)
p2 = GPIO.PWM(13, f2)
p1.start(dc1)
p2.start(dc2)
def GPIO17_callback(channel):
    """
    interrupt handler for GPIO17; button on piTFT
    """ 
    global p1
    p1.ChangeDutyCycle(170/2170.0*100)
    p1.ChangeFrequency(100000/2170.0)
    print "in interrupt 17"


def GPIO22_callback(channel):
    """
    interrupt handler for GPIO22; button on piTFT
    """
    global p1
    p1.ChangeDutyCycle(150/2150.0*100)
    p1.ChangeFrequency(100000/2150.0)
    print "in interrupt 22"


def GPIO23_callback(channel):
    """
    interrupt handler for GPIO23; button on piTFT
    """
    global p1
    p1.ChangeDutyCycle(130/2130.0*100)
    p1.ChangeFrequency(100000/2130.0)
    print "in interrupt 23"


def GPIO27_callback(channel):
    """
    interrupt handler for GPIO27; button on piTFT
    """

    global p2
    p2.ChangeDutyCycle(170/2170.0*100)
    p2.ChangeFrequency(100000/2170.0)
    print "in interrupt 27"

def GPIO26_callback(channel):
    """
    interrupt handler for GPIO26; external button
    """
    global p2
    p2.ChangeDutyCycle(150/2150.0*100)
    p2.ChangeFrequency(100000/2150.0)
    print "in interrupt 26"


def GPIO19_callback(channel):
    """
    interrupt handler for GPIO19; external button
    """    
    global p2
    p2.ChangeDutyCycle(130/2130.0*100)
    p2.ChangeFrequency(100000/2130.0)
    print "in interrupt 19"
    
# Setup the GPIO pins as interrupts
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, callback=GPIO19_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)


try:
    time.sleep(15)
except KeyboardInterrupt:
    GPIO.cleanup() #cleans the GPIO in case of usage of CTRL C
    print 
#If exit button pressed. Exit video and terminate code


GPIO.cleanup()    
