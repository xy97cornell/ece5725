# screen_coordinates.py
# 10/4/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
# Lab 02
#
# Display a single quit button at the bottom of the screen
# Tapping any location on the screen still display ‘Hit at x, y’ 
# Saves every 20 hits in a list and prints it out as well
# where x, y show the screen coordinates of the hit. 
# Tapping the ‘quit’ button will exit the program. 
# All locations display in the linux console
# There is a physical bail-out button for this code.
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
#BAIL OUT BUTTON
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO17_callback(channel):
    """Bail our button interrupt"""
    print "in interrupt 17"
    global code_running
    code_running = False

coord_lst = [] #store the hit coordinates

GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
size = width, height = 320, 240
BLACK = 0, 0, 0
WHITE = 255,255,255
screen = pygame.display.set_mode(size)
pygame.init()
my_font = pygame.font.Font(None,50)
my_buttons = {'Quit':(160, 200)} #physical quit button
font2 = pygame.font.Font(None,30)
screen.fill(BLACK) # Erase the Work space

#place the buttons in dictionary on screen
for my_text,text_pos in my_buttons.items():
    text_surface = my_font.render(my_text,True,WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)
pygame.display.flip()

while(code_running):
    for event in pygame.event.get():
        if(event.type is pygame.MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
    
        if(event.type is pygame.MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x, y = pos
            print(x,y)
            if y > 150 and x>75 and x<250:
                code_running = False
            else: 
                pygame.draw.rect(screen, black, pygame.Rect(50, 0, 250, 120))
                pygame.display.flip()
                text_surface = font2.render("Position = ("+str(x)+","+str(y)+")",True,WHITE)
                rect = text_surface.get_rect(center=(160, 100))
                screen.blit(text_surface,rect)
                pygame.display.flip()
                coord_lst.append(pos)
                if(len(coord_lst)>=20):
                    print(coord_lst)
                    coord_lst=[] #reset


GPIO.cleanup()	
