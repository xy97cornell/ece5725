#
# jfs9 9/10/17  GPIO example python script
#
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
# setup piTFT buttons
#                        V need this so that button doesn't 'float'!
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.2)  # Without sleep, no screen output!
    if ( not GPIO.input(26) ):
        print (" ") 
        print "Button 26 pressed...."
