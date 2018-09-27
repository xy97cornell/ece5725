import RPi.GPIO as GPIO
import time
import subprocess
import threading
import thread
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
wait_time = 0.00002
'''
def end():
    #subprocess.call('echo "quit" > video_fifo', shell=True)
    print('!!!')
    thread.interrupt_main()
threading.Timer(1, end).start()
'''
class timer(threading.Thread):
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
while True:
    #time.sleep(wait_time)
    i1 = GPIO.input(17)
    i2 = GPIO.input(22)
    i3 = GPIO.input(23)
    i4 = GPIO.input(27)
    i5 = GPIO.input(26)
    i6 = GPIO.input(19)
    if i1 == 0:  
        time.sleep(0.05)
        i1 = GPIO.input(17)
        if i1 == 0:
            subprocess.call('echo "pause" > video_fifo &', shell=True)
    elif i2 == 0:
        time.sleep(0.05)
        i2 = GPIO.input(22)
        if i2 == 0:
            subprocess.call('echo "seek 10 0" > video_fifo &', shell=True)
    elif i3 == 0:
        time.sleep(0.05)
        i3 = GPIO.input(23)
        if i3 == 0:
            subprocess.call('echo "seek -10 0" > video_fifo &', shell=True)
   
    elif i4 == 0:
        time.sleep(0.05)
        i4 = GPIO.input(27)
        if i4 == 0:
            subprocess.call('echo "quit" > video_fifo &', shell=True)
            break
   
    elif i5 == 0:
        time.sleep(0.05)
        i5 = GPIO.input(26)
        if i5 == 0:
            subprocess.call('echo "seek" 30 0 > video_fifo &', shell=True)

    elif i6 == 0:
        time.sleep(0.05)
        i6 = GPIO.input(19)
        if i6 == 0:
            subprocess.call('echo "seek" -30 0 > video_fifo &', shell=True)

