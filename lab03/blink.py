
import RPi.GPIO as GPIO
import time
frequency = 0.5 
dc = 50

GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.OUT)
p = GPIO.PWM(5, frequency)
code_running = True
 
p.start(dc) # where dc is the duty cycle (0.0 <= dc <= 100.0)

#ip.ChangeFrequency(freq) # where freq is the new frequency in Hz

#p.ChangeDutyCycle(dc) # where 0.0 <= dc <= 100.0

#p.stop()

#p = GPIO.PWM(GPIO_pin, frequency)
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
