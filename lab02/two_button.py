# two_button.py
# 10/4/18 
# Lab 02
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# Two, on-screen buttons are displayed ‘start’ and ‘quit’
# Hitting ‘start’ begins playback of two_collide.py
# Hitting ‘quit’ ends the program and returns to the Linux console screen.
# Hitting any other location on the screen displays screen coordinates.
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
time_limit = 15 #second
start_time = time.time()
code_running = True
black = 0, 0, 0
#BAIL OUT BUTTON
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO17_callback(channel):
    """Bail out button interrupt"""
    print "in interrupt 17"
    global code_running
    code_running = False

def elastic(speed1,speed2):
    """
    Swap the values of speed1 and speed2
    para: speed1 and speed2 are list with 2 values: x and y speeds
    """
    tmp = [speed1[0], speed1[1]]
    speed1[0] = speed2[0]
    speed1[1] = speed2[1]
    speed2[0] = tmp[0]
    speed2[1] = tmp[1]

# Set up interrupt
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
size = width, height = 320, 240
BLACK = 0, 0, 0
WHITE = 255,255,255
screen = pygame.display.set_mode(size)
pygame.init()
my_font = pygame.font.Font(None,30)

#init the two buttons for PiTFT
my_buttons = {'Start':(80, 220), 'Quit':(240, 220)}
screen.fill(BLACK) # Erase the Work space
for my_text,text_pos in my_buttons.items():
    text_surface = my_font.render(my_text,True,WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)
pygame.display.flip()
animation_running = False # animation running state
paused = False # For checking if we are paused; pause state
sleeptime = 0.02 # For artificially setting the FPS

size2 = width2, height2 = 320, 200
speed1 = [1, 2]
speed2 = [3, 1]
black = 0, 0, 0
ball1 = pygame.image.load("../../python_games/gem1.png")
ball2 = pygame.image.load("../../python_games/gem2.png")
# init balls 
balls = [ball1, ball2]
ballrect = balls[0].get_rect()
ballrect.x = 50
ballrect.y = 50

ballrect2 = balls[1].get_rect()
ballrect2.x = 150
ballrect2.y = 100
while(code_running):
    for event in pygame.event.get():
        if(event.type is pygame.MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        if(event.type is pygame.MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x, y = pos
            print(x,y) #Debug printing our mouse pos
            if y > 150:
                if x > 160: #checking range for x location
                    code_running = False
                else:
                    animation_running = True
            else: #when we didn't press the start or quit button
                pygame.draw.rect(screen, black, pygame.Rect(50, 0, 250, 120))
                pygame.display.flip()
                text_surface = my_font.render("Position = \
                ("+str(x)+","+str(y)+")",True,WHITE)
                rect = text_surface.get_rect(center=(160, 100))
                screen.blit(text_surface,rect)
                pygame.display.flip()

    if animation_running: #two_collide.py code controlling ball movements
        pygame.draw.rect(screen, black, pygame.Rect(0, 0, 320, 200))
        ballrect = ballrect.move(speed1)
        if ballrect.left < 0 or ballrect.right > width2:
            speed1[0] = -speed1[0]
        if ballrect.top < 0 or ballrect.bottom > height2:
            speed1[1] = -speed1[1]
        ballrect2 = ballrect2.move(speed2)
        if ballrect2.left < 0 or ballrect2.right > width2:
            speed2[0] = -speed2[0]
        if ballrect2.top < 0 or ballrect2.bottom > height2:
            speed2[1] = -speed2[1]
        if(ballrect2.colliderect(ballrect)):
            elastic(speed1,speed2)	
        
        screen.blit(ball1, ballrect)
        screen.blit(ball2, ballrect2)
        pygame.display.flip()
        time.sleep(sleeptime) #control frame rate which slows down the ball display
            
GPIO.cleanup()	
