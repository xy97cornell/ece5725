#
# jfs9, 2/23/18 GPIO example python script
#
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
# setup piTFT buttons
#                        V need this so that button doesn't 'float'!
#GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    time.sleep(1.0) # sleep a bit...
    print "tick.."
    if ( not GPIO.input(26) ):
        print (" ") 
        print "Button 26 pressed...."
