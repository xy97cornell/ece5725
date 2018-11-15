
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


GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
size = width, height = 320, 240
BLACK = 0, 0, 0
WHITE = 255,255,255
screen = pygame.display.set_mode(size)
pygame.init()
my_font = pygame.font.Font(None,50)
# First level buttons
my_buttons = {'Start':(80, 200), 'Quit':(240, 200)}
font2 = pygame.font.Font(None, 30)
# Four new buttons of the second level
four_buttons = {"Pause":(40, 220), "Fast":(110, 220), "Slow":(180, 220), "Back":(250,220)}
screen.fill(BLACK) # Erase the Work space

# collect the texts for first level
for my_text,text_pos in my_buttons.items():
    text_surface = my_font.render(my_text,True,WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)
pygame.display.flip()
animation_running = False # animation running state
paused = False # For checking if we are paused; pause state
sleeptime = 0.02 # For artificially setting the FPS

while(code_running):
    # If we are in the starting state where no animation is running
    if animation_running == False:
        for event in pygame.event.get():
            if(event.type is pygame.MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
            if(event.type is pygame.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x, y = pos
                print(x,y)
                if y > 150: #poll for button presses
                    if x > 160:
                        code_running = False
                        #QUITING to Linux Terminal
                    else:
                        animation_running = True
                else: #display coordinates
                    pygame.draw.rect(screen, black, pygame.Rect(50, 0, 250, 120))
                    pygame.display.flip()
                    text_surface = font2.render("Position = \
                    ("+str(x)+","+str(y)+")",True,WHITE)
                    rect = text_surface.get_rect(center=(160, 100))
                    screen.blit(text_surface,rect)
                    pygame.display.flip()
    else: #When animation is running 
        #Must init balls like in two_collide.py
        screen.fill(black)
        size2 = width2, height2 = 320, 200
        speed1 = [1, 2]
        speed2 = [3, 1]
        black = 0, 0, 0
        ball1 = pygame.image.load("../../python_games/gem1.png")
        ball2 = pygame.image.load("../../python_games/gem2.png")
        balls = [ball1, ball2]
        ballrect = balls[0].get_rect()
        ballrect.x = 50
        ballrect.y = 50
        
        ballrect2 = balls[1].get_rect()
        ballrect2.x = 150
        ballrect2.y = 100
        # Look in the second level buttons dict to draw the button rectangles
        for my_text,text_pos in four_buttons.items():
            text_surface = font2.render(my_text,True,WHITE)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
            pygame.display.flip()
        
        while animation_running and code_running:
            #state for running animation where we poll for the control button pressed
            for event in pygame.event.get():
                if(event.type is pygame.MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                if(event.type is pygame.MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    print(x,y)
                    if y > 200:
                        if x < 80: #poll for paused button
                            paused = ~paused
                            pygame.draw.rect(screen, black, pygame.Rect(0, 200, 90, 40))
                            if paused: #change display text 
                                text_surface = font2.render("Continue",True,WHITE)
                            else:
                                text_surface = font2.render("Pause",True,WHITE)
                            rect = text_surface.get_rect(center=(40, 220))
                            screen.blit(text_surface,rect)
                            pygame.display.flip()
                        elif x > 80 and x < 160: #check for faster
                            sleeptime = max(sleeptime*0.5, 0.001)
                        elif x > 160 and x < 240: #check for slower
                            sleeptime = min(sleeptime*2, 0.1)
                        elif x > 240: #backing out of second level
                            screen.fill(black)
                            for my_text,text_pos in my_buttons.items():
                                text_surface = my_font.render(my_text,True,WHITE)
                                rect = text_surface.get_rect(center=text_pos)
                                screen.blit(text_surface,rect)
                            pygame.display.flip()
                            animation_running = False
                 #for ballrect in ballrects:
            if not paused and animation_running: #only will update if we are not paused
                #and animation has been set to running
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
                
                pygame.draw.rect(screen, black, pygame.Rect(0, 0, 320, 200))
                screen.blit(ball1, ballrect)
                screen.blit(ball2, ballrect2)
                pygame.display.flip()
            time.sleep(sleeptime)
            
GPIO.cleanup()	
