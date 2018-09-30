# quit_button.py
# 10/4/18 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
#
# Initializes a single on screen button using Pygame
# Displays the "quit" button on screen where if you tap it,
# the program quits to the command shell. It stays in the polling
# state for 30 seconds and the exits. 
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

start_time = time.time()
time_limit = 30

pygame.init()
pygame.mouse.set_visible(False)
code_running = True
black = 0, 0, 0
#BAIL OUT BUTTON
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO17_callback(channel):
    """
    Bail out interrupt in case code breaks
    """
    print "in interrupt 17"
    global code_running
    code_running = False

#set up interrupt for GPIO for bail out
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
size = width, height = 320, 240
BLACK = 0, 0, 0
WHITE = 255,255,255
screen = pygame.display.set_mode(size)
pygame.init()
my_font = pygame.font.Font(None,50)
my_buttons = {'Quit':(160, 200)}
screen.fill(BLACK) # Erase the Work space

#Display the texts by rendering it and then bliting it
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
            if y > 150 and x>70 and x<250:
                # narrow down the range of pos
                code_running = False 
        #check if reached time limit        
        if(time.time()-start_time >= time_limit):
            code_running = False
            
GPIO.cleanup()	
