# control_two_collide.py
# 10/4/18 
# Lab 02
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# Two levels of menu: 
#   main:
#     start and quit button like in two_button.py
#       Hitting ‘start’ begins playback of two_collide.py
#       Hitting ‘quit’ ends the program and returns to the Linux 
#       console screen.
#   control: 
#     After hitting 'start', displays four new options:
#       Pause/restart: pause a running animation. Restart a paused animation
#       Faster: speed up the animation by a fixed amount
#       Slower: slow the animation by a fixed amount
#       Back: stop the animation and return to the ‘top’ menu screen which
# 
# Contains a physical bail-out button for this code.
# 

import time
import RPi.GPIO as GPIO
import os
import pygame
import subprocess

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 

os.putenv('SDL_MOUSEDRV', 'TSLIB') #setup mouse in pygame
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen') #touchscreen as mouse

pygame.init()
pygame.mouse.set_visible(False)
code_running = True
black = 0, 0, 0

#GPIO RELATED
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



BLACK = 0, 0, 0
WHITE = 255,255,255
screen = pygame.display.set_mode(size)
pygame.init()
my_font = pygame.font.Font(None,50)
# First level buttons
my_buttons = {'Stop':(180, 120), 'Quit':(240, 220), 'Resume':(180, 120)}
# Four new buttons of the second level
screen.fill(BLACK) # Erase the Work space

left_history = []
right_history = []
for i in range(0, 3):
    left_history.append(("", 0))
    right_history.append(("", 0))

# collect the texts for first level
for i in [0, 1]:
    text_surface = my_font.render(my_buttons[i],True,WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)
pygame.display.flip()
paused = False # For checking if we are paused; pause state
sleeptime = 0.02 # For artificially setting the FPS


try:
    while(code_running):
        # If we are in the starting state where no animation is running

        if paused == False:
            for event in pygame.event.get():
                if(event.type is pygame.MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                if(event.type is pygame.MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    print(x,y)
                    if y > 100 and y < 140: #poll for button presses
                        if x > 160 and x < 200:
                            paused = True
                            #QUITING to Linux Terminal
                    if y > 200 and y < 240:
                        if x > 220 and x < 260:
                            code_running = False
                    if y 
        else: #When animation is running 
            #Must init balls like in two_collide.py
            # Look in the second level buttons dict to draw the button rectangles             
            for event in pygame.event.get():
                if(event.type is pygame.MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                if(event.type is pygame.MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    print(x,y)
                    if y > 100 and y < 140: #poll for button presses
                        if x > 160 and x < 200:
                            paused = False
                            #QUITING to Linux Terminal
                    if y > 200 and y < 240:
                        if x > 220 and x < 260:
                            code_running = False
        time.sleep(sleeptime)
except KeyboardInterrupt:
    code_running = False
GPIO.cleanup()	
