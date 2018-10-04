
import RPi.GPIO as GPIO
import time
import sys 


frequency = 100000/(150 + 2000.0)
dc = 150/(150 + 2000.0)*100
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.OUT)
p = GPIO.PWM(13, frequency)
code_running = True
 
def GPIO17_callback(channel):
    GPIO.cleanup()
    sys.exit(1);
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
#GPIO.wait_for_edge(17, GPIO.FALLING)
p.start(dc) # where dc is the duty cycle (0.0 <= dc <= 100.0)

#ip.ChangeFrequency(freq) # where freq is the new frequency in Hz

#p.ChangeDutyCycle(dc) # where 0.0 <= dc <= 100.0
#p.stop()

#p = GPIO.PWM(GPIO_pin, frequency)
time.sleep(10)
    
GPIO.cleanup()
