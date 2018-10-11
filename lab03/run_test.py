import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
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
#forward
p1.ChangeDutyCycle(130/2130.0*100)
p1.ChangeFrequency(100000/2130.0)
p2.ChangeDutyCycle(130/2130.0*100)
p2.ChangeFrequency(100000/2130.0)
time.sleep(3)
#stop
p1.ChangeDutyCycle(150/2150.0*100)
p1.ChangeFrequency(100000/2150.0)
p2.ChangeDutyCycle(150/2150.0*100)
p2.ChangeFrequency(100000/2150.0)
time.sleep(1)
#backforward
p1.ChangeDutyCycle(170/2170.0*100)
p1.ChangeFrequency(100000/2170.0)
p2.ChangeDutyCycle(170/2170.0*100)
p2.ChangeFrequency(100000/2170.0)
time.sleep(3)
#left_turn
p1.ChangeDutyCycle(150/2150.0*100)
p1.ChangeFrequency(100000/2150.0)
p2.ChangeDutyCycle(130/2130.0*100)
p2.ChangeFrequency(100000/2130.0)
time.sleep(3)
#right_turn
p1.ChangeDutyCycle(130/2130.0*100)
p1.ChangeFrequency(100000/2130.0)
p2.ChangeDutyCycle(150/2150.0*100)
p2.ChangeFrequency(100000/2150.0)
time.sleep(3)
