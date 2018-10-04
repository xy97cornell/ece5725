# two_bounce.py
# 10/4/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
# Lab 02
#
# Initalizes Pygame and draws two ball to bounce around on 
# a black canvas. 
# No collision detection between balls. Only
# detection between boundaries
# The animation runs on the monitor 
# The animation runs forever  
#  


import pygame # Import pygame graphics library
import os # for OS calls

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0') 

size = width, height = 320, 240
speed1 = [2,2]
speed2 = [5,5]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball1 = pygame.image.load("../../python_games/gem1.png")
ball2 = pygame.image.load("../../python_games/gem2.png")

balls = [ball1,ball2] # List of balls

ballrect = balls[0].get_rect() #init first ball
ballrect.x = 50
ballrect.y = 50

ballrect2 = balls[1].get_rect() #inti second ball
ballrect2.x = 150
ballrect2.y = 150


while 1:
	
	# check for boundary collision of first ball
    ballrect = ballrect.move(speed1)
    if ballrect.left < 0 or ballrect.right > width:
        speed1[0] = -speed1[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed1[1] = -speed1[1]
    
	# check for boundary collision of second ball
    ballrect2 = ballrect2.move(speed2)
    if ballrect2.left < 0 or ballrect2.right > width:
        speed2[0] = -speed2[0]
    if ballrect2.top < 0 or ballrect2.bottom > height:
        speed2[1] = -speed2[1]
    
    
    screen.fill(black) # Erase the Work space

    screen.blit(ball1, ballrect) # Combine Ball surface with workspace surface
    screen.blit(ball2, ballrect2) # Combine Ball surface with workspace surface
    
    pygame.display.flip() # display workspace on screen
