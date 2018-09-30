# two_collide.py
# 10/4/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# Initalizes Pygame and draws two ball to bounce around on 
# a black canvas. 
# Collision detection between balls and boundary
# The animation runs on the PiTFT 
# The animation runs forever 
# Physical buttons as bailout buttons on the side of PiTFT
#  

import pygame # Import pygame graphics library
import os # for OS calls
import sys
import RPi.GPIO as GPIO
import time

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 

#Setup GPIO for breakout
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
flag = True  #flag for staying in while loop       

def GPIO17_callback(channel):
    """Bail out button interrupt"""
    print "in interrupt 17"
    global flag
    flag = False

def GPIO22_callback(channel):
    """Bail out button interrupt"""
    print "in interrupt 22"
    global flag
    flag = False


def GPIO23_callback(channel):
    """Bail out button interrupt"""
    print "in interrupt 23"
    global flag
    flag = False

def GPIO27_callback(channel):
    """Bail out button interrupt"""
    print "in interrupt 27"
    global flag
    flag = False

#set up GPIO buttons as interrupts
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)


size = width, height = 320, 240
speed1 = [1,1] 
speed2 = [3,3]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball1 = pygame.image.load("../../python_games/gem1.png")
ball2 = pygame.image.load("../../python_games/gem2.png")

balls = [ball1,ball2]

ballrect = balls[0].get_rect()
ballrect.x = 50
ballrect.y = 50

ballrect2 = balls[1].get_rect()
ballrect2.x = 150
ballrect2.y = 150

def elastic(speed1,speed2):
    """
    Swap the values of speed1 and speed2
    para: speed1 and speed2 are list with 2 values: x and y speeds
    """
    tmp = [speed1[0],speed1[1]] 
    speed1[0] = speed2[0]
    speed1[1] = speed2[1]
    speed2[0] = tmp[0]
    speed2[1] = tmp[1]
    
     

while flag:
	
    #adjust speed of ballrect1
    ballrect = ballrect.move(speed1)
    if ballrect.left < 0 or ballrect.right > width:
        speed1[0] = -speed1[0]
		
	
    if ballrect.top < 0 or ballrect.bottom > height:
        speed1[1] = -speed1[1]
	
    #adjust speed of ballrect2
    ballrect2 = ballrect2.move(speed2)
    if ballrect2.left < 0 or ballrect2.right > width:
		speed2[0] = -speed2[0]

    if ballrect2.top < 0 or ballrect2.bottom > height:
		speed2[1] = -speed2[1]

    if(ballrect2.colliderect(ballrect)): #check if ball collided
        elastic(speed1,speed2)	
		
    screen.fill(black) # Erase the Work space

    screen.blit(ball1, ballrect) # Combine Ball surface with workspace surface
    screen.blit(ball2, ballrect2) # Combine Ball surface with workspace surface
    
    pygame.display.flip() # display workspace on screen


    time.sleep(0.01) #Sets the framerate by artificially causing delay


GPIO.cleanup()	

