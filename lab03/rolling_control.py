# rolling_control.py
# 10/18/18 
# Lab 03
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# Displays direction (clockwise, counter-clockwise, 
# stopped) for each motor
# Displays a single, red ‘panic stop’ button on the piTFT. 
# If pressed, motors
# immediately stop and ‘panic stop’ changes to a green 
# ‘resume’ button
# Displays a ‘quit’ button on the piTFT. When hit, quit 
# causes the program to end
# and control returns to the Linux console screen.
# Records start-time/direction pairs for each motor 
# and display a scrolling history of the most recent 
# motion (include 3 past entries for each motor).
# 
# 

import time
import RPi.GPIO as GPIO
import os
import pygame
import subprocess

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 

os.putenv('SDL_MOUSEDRV', 'TSLIB') #setup mouse in pygame
#touchscreen as mouse
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen') 

pygame.init()
pygame.mouse.set_visible(False)
size = 320, 240
code_running = True
paused = False
start_time = time.time()
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

#START SERVO IN STOP POSITION
dc1 = 150/2150.0*100
dc2 = 150/2150.0*100
f1 = 100000/2150.0
f2 = 100000/2150.0
p1 = GPIO.PWM(6, f1)
p2 = GPIO.PWM(13, f2)
p1.start(dc1)
p2.start(dc2)
left_history = [("Stop        ",0), ("Stop        ",0),\
 ("Stop        ",0)]
right_history = [("Stop        ",0), ("Stop        ",0),\
 ("Stop        ",0)]
def GPIO17_callback(channel):
    """
    interrupt handler for GPIO17; button on piTFT
    """ 
    global p1 
    global left_history
    global paused
    if not paused:
        left_history.insert(0, ("Counter-Clk ", \
        int(time.time() - start_time)))
        p1.ChangeDutyCycle(170/2170.0*100)
        p1.ChangeFrequency(100000/2170.0)
        left_history.pop()
        print "in interrupt 17"


def GPIO22_callback(channel):
    """
    interrupt handler for GPIO22; button on piTFT
    """
    global p1
    global left_history
    global paused
    if not paused: 
        left_history.insert(0, ("Stop        ",\
         int(time.time() - start_time)))
        p1.ChangeDutyCycle(150/2150.0*100)
        p1.ChangeFrequency(100000/2150.0)
        left_history.pop()
        print "in interrupt 22"


def GPIO23_callback(channel):
    """
    interrupt handler for GPIO23; button on piTFT
    """
    global p1
    global left_history
    global paused
    if not paused:
        left_history.insert(0, ("Clkwise      ",\
         int(time.time() - start_time))) 
        p1.ChangeDutyCycle(130/2130.0*100)
        p1.ChangeFrequency(100000/2130.0)
        left_history.pop()
        print "in interrupt 23"


def GPIO27_callback(channel):
     
    global p2
    global right_history
    global paused
    if not paused:
        right_history.insert(0, ("Counter-Clk ",\
         int(time.time() - start_time)))
        p2.ChangeDutyCycle(170/2170.0*100)
        p2.ChangeFrequency(100000/2170.0) 
        right_history.pop()
        print "in interrupt 27"

def GPIO26_callback(channel):
    """
    interrupt handler for GPIO26; external button
    """
    global p2
    global right_history
    global paused
    if not paused:
        right_history.insert(0, ("Stop        ",\
         int(time.time() - start_time)))
        p2.ChangeDutyCycle(150/2150.0*100)
        p2.ChangeFrequency(100000/2150.0)
        right_history.pop()
        print "in interrupt 26"


def GPIO19_callback(channel):
    """
    interrupt handler for GPIO19; external button
    """    
    global p2
    global right_history
    global paused
    if not paused: 
        right_history.insert(0, ("Clkwise      ",\
         int(time.time() - start_time)))
        p2.ChangeDutyCycle(130/2130.0*100)
        p2.ChangeFrequency(100000/2130.0)
        right_history.pop()
        print "in interrupt 19"
    
# Setup the GPIO pins as interrupts
GPIO.add_event_detect(17, GPIO.FALLING, \
callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, \
callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, \
callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, \
callback=GPIO26_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, \
callback=GPIO19_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, \
callback=GPIO27_callback, bouncetime=300)



BLACK = 0, 0, 0
WHITE = 255,255,255
RED = 255, 0, 0
GREEN = 0, 255, 255
screen = pygame.display.set_mode(size)
pygame.init()
font1 = pygame.font.Font(None, 40)
font2 = pygame.font.Font(None, 20)
font3 = pygame.font.Font(None, 30)
screen.fill(BLACK) # Erase the Work space
pygame.draw.circle(screen, RED, (160, 120), 30)

text_surface = font1.render("STOP", True, WHITE)
rect = text_surface.get_rect(center=(160, 120))
screen.blit(text_surface, rect)

text_surface = font2.render("QUIT", True, WHITE)
rect = text_surface.get_rect(center=(240, 220))
screen.blit(text_surface, rect)

text_surface = font2.render("Left History", True, WHITE)
rect = text_surface.get_rect(center=(50, 25))
screen.blit(text_surface, rect)

text_surface = font2.render("Right History", True, WHITE)
rect = text_surface.get_rect(center=(270, 25))
screen.blit(text_surface, rect)

pygame.display.flip()
sleeptime = 0.02 # For artificially setting the FPS

positions1 = [(50, 80), (50, 120), (50, 160)]
positions2 = [(260, 80), (260, 120), (260, 160)]


while(code_running):
    try:
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 50, 110, 200))
        pygame.draw.rect(screen, BLACK, pygame.Rect(210, 50, 100, 200))
        text_surface = font2.render("QUIT", True, WHITE)
        rect = text_surface.get_rect(center=(240, 220))
        screen.blit(text_surface, rect)
        for i in range(0, 3): #displaying the history on the screen
            title, record = left_history[i]
            text_surface = font2.render(title + ":" + str(record), True, WHITE)
            rect = text_surface.get_rect(center=positions1[i])
            screen.blit(text_surface, rect)

            title, record = right_history[i]
            text_surface = font2.render(title + ":" + str(record), True, WHITE)
            rect = text_surface.get_rect(center=positions2[i])
            screen.blit(text_surface, rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if(event.type is pygame.MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
            if(event.type is pygame.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x, y = pos
                if y > 100 and y < 140: #poll for button presses
                    if x > 120 and x < 200:
                        paused = not paused
                        pygame.draw.rect(screen, BLACK, pygame.Rect(110, 90, 100, 70))
                        if paused == True: #If paused, we must stop and save state. 
                            p1.ChangeDutyCycle(150/2150.0*100)
                            p1.ChangeFrequency(100000/2150.0)
                            p2.ChangeDutyCycle(150/2150.0*100)
                            p2.ChangeFrequency(100000/2150.0)
                            pygame.draw.circle(screen, GREEN, (160, 120), 30)
                            text_surface = font3.render("RESUME", True, WHITE)
                            rect = text_surface.get_rect(center=(160, 120))        
                            screen.blit(text_surface, rect)
                        else:
                            pygame.draw.circle(screen, RED, (160, 120), 30)
                            text_surface = font1.render("STOP", True, WHITE)
                            rect = text_surface.get_rect(center=(160, 120))        
                            screen.blit(text_surface, rect)
                        pygame.display.flip()
                        
                        #QUITING to Linux Terminal
                if y > 200 and y < 240:
                    if x > 220 and x < 260:
                        code_running = False 
        time.sleep(sleeptime)
        if time.time() - start_time > 30:
            break
    except KeyboardInterrupt:
        code_running = False

GPIO.cleanup()	
