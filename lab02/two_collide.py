import pygame # Import pygame graphics library
import os # for OS calls
import sys
import RPi.GPIO as GPIO
import time

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 
#os.clock.tick(30)
#Setup GPIO for breakout
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
flag = True        

def GPIO17_callback(channel):
    print "in interrupt 17"
    #os._exit(1)
    #quit()
    global flag
    flag = False

def GPIO22_callback(channel):
    print "in interrupt 22"
    #os._exit(1)
    #quit()
    global flag
    flag = False


def GPIO23_callback(channel):
    print "in interrupt 23"
#    os._exit(1)
    #quit()
    global flag
    flag = False

def GPIO27_callback(channel):
    print "in interrupt 27"
#    os._exit(1)
    #quit()
    global flag
    flag = False


GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)

start_time = time.time()
end_time = 10

size = width, height = 320, 240
speed1 = [1,1]#[5,5]#
speed2 = [1,1]#[2,2]
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
    tmp = [speed1[0],speed1[1]]
    if ballrect.colliderect(ballrect2): 
		
        speed1[0] = speed2[0]
        speed1[1] = speed2[1]
        speed2[0] = tmp[0]
        speed2[1] = tmp[1]
        

while flag:
	 #for ballrect in ballrects:
    ballrect = ballrect.move(speed1)
    if ballrect.left < 0 or ballrect.right > width or ballrect.colliderect(ballrect2):
        #elastic(speed1, speed2)
        speed1[0] = -speed1[0]
		
	
    if ballrect.top < 0 or ballrect.bottom > height or ballrect.colliderect(ballrect2):
        #elastic(speed1, speed2)
        speed1[1] = -speed1[1]
		
    ballrect2 = ballrect2.move(speed2)
    if ballrect2.left < 0 or ballrect2.right > width or ballrect2.colliderect(ballrect):
		#elastic(speed1, speed2)
		speed2[0] = -speed2[0]

    if ballrect2.top < 0 or ballrect2.bottom > height or ballrect2.colliderect(ballrect):
		#elastic(speed1, speed2)
		speed2[1] = -speed2[1]

    if(ballrect2.colliderect(ballrect)):
        elastic(speed1,speed2)	
		
    screen.fill(black) # Erase the Work space

    screen.blit(ball1, ballrect) # Combine Ball surface with workspace surface
    screen.blit(ball2, ballrect2) # Combine Ball surface with workspace surface
    
    pygame.display.flip() # display workspace on screen

    #if(time.time()-start_time>end_time):
    #	quit()


GPIO.cleanup()	

