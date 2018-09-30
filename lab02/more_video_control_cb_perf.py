# more_video_control_cb_perf.py
# 10/4/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# Testing setup for perf with more_video_control_cb.py
# runs the file for 10 seconds with perf called 
# externally. This one runs with the interrupts
#


import RPi.GPIO as GPIO
import time
import subprocess
import threading
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def GPIO17_callback(channel):
    print "in interrupt 17"
    subprocess.call('echo "pause" > video_fifo', shell=True)


def GPIO22_callback(channel):
    print "in interrupt 22"
    subprocess.call('echo "seek 10 0" > video_fifo', shell=True)


def GPIO23_callback(channel):
    print "in interrupt 23"
    subprocess.call('echo "seek -10 0" > video_fifo', shell=True)


def GPIO27_callback(channel):
    print "in interrupt 27"
    subprocess.call('echo "quit" > video_fifo', shell=True)

def GPIO26_callback(channel):
    print "in interrupt 26"
    subprocess.call('echo "seek" 30 0 > video_fifo', shell=True)


def GPIO19_callback(channel):
    print "in interrupt 19"
    subprocess.call('echo "seek" -30 0 > video_fifo', shell=True)
    

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, callback=GPIO19_callback, bouncetime=300)

class timer(threading.Thread):
    """
    Timer class used to exit the program when a certain time limit 
    has been reached
    """

    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        time.sleep(10)
        subprocess.call('echo "quit" > video_fifo &', shell=True)
        os._exit(1)
        return
    def stop(self):
        self._stop_event.set()

timer().start()
GPIO.wait_for_edge(27, GPIO.FALLING)
