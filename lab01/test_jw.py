import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    i1 = GPIO.input(17)
    i2 = GPIO.input(22)
    i3 = GPIO.input(23)
    i4 = GPIO.input(27)
    if i1 == 0:
        subprocess.call('echo "pause" > video_fifo', shell=True)
        time.sleep(1)
    elif i2 == 0:
        subprocess.call('echo "seek 10 0" > video_fifo', shell=True)
        time.sleep(1)
    elif i3 == 0:
        subprocess.call('echo "seek -10 0" > video_fifo', shell=True)
        time.sleep(1)
    elif i4 == 0:
        subprocess.call('echo "quit" > video_fifo', shell=True)
        quit()

