# mainserver_v2.py
# 12/7/2018 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
# Final Project - Telepresence Robot
#
# Main control for the basestation. Handles communication with robot 
# through bluetooth, then receives camera data from the robot. Also 
# displays the camera images to the PiTFT and any GUI.
# 


import socket
import sys
import subprocess
import re
import time
import threading
import cv2
import numpy as np
import requests
from PIL import Image
from bluedot.btcomm import BluetoothServer, BluetoothAdapter

import RPi.GPIO as GPIO
import pygame
import os
import bno #custom module

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 
os.putenv('SDL_MOUSEDRV', 'TSLIB') #setup mouse in pygame
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen') #touchscreen as mouse



result = subprocess.run('hostname -I', stdout=subprocess.PIPE, 
shell=True)
result = result.stdout.decode('utf-8')
host_IP = re.split(' |\n', result)[0]
print("host_IP: "+host_IP)

result = subprocess.run('hcitool dev|grep hci0', stdout=subprocess.PIPE, 
shell=True)
result = result.stdout.decode('utf-8')
host_mac = re.split(' |\n|\t', result)[2]
print("host_mac: "+host_mac)

client_IP = '10.148.4.162' #default Client IP

code_running = True
turn = 0

#######GPIO CALLBACK FUNCTIONS (Interrupt Handlers)############
def GPIO22_callback(channel):
    """
    interrupt handler for GPIO17; button on piTFT
    Sets the control enabled bit for whether we are turning on 
    motion controls on the robot
    """
    print ("in interrupt 22")
    global turn 
    turn = 1 if turn==0 else 0
    

def GPIO23_callback(channel):
    """
    Unused
    """
    print ("in interrupt 23")
    
    
    
def GPIO27_callback(channel):
    """
    Exits the program. Breakout button
    """
    print ("in interrupt 27")
    global code_running
    code_running = False
    GPIO.cleanup()
    sys.exit(0)
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(22,GPIO.FALLING,callback=GPIO22_callback,
bouncetime=300)
GPIO.add_event_detect(23,GPIO.FALLING,callback=GPIO23_callback,
bouncetime=300)
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback,
bouncetime=300)

size = 320,240
screen = pygame.display.set_mode(size)
pygame.init()

pygame.mouse.set_visible(False)
my_font = pygame.font.Font(None,30)

COMMAND_PORT=5000
CAM_PORT = 8000
BUFFER_SIZE = 1024
get_ip()
time.sleep(2)

def data_received(data):
    """
    Callback fuction for receiving bluetooth messages
    """
    global client_IP
    global flag
    global blue
    print("Got IP from Client! IP: "+ str(data))
    client_IP = data
    flag = False

def get_ip():
    """
    Receives sender IP through bluetooth
    Relays its IP back to the sender using send's IP that was 
    received
    Also generates pygame GUI to inform user that we are looking
    for bluetooth.
    Blocks until one robot connects 
    """
    global flag
    blue =  BluetoothServer(data_received, power_up_device=True)
    flag = True
    i = 0
    while flag:
        screen.fill((0,0,0))
        mytext = "Connecting to Bluetooth"
        
        if(i==0):
            mytext = mytext+'.'
        elif (i==1):
            mytext = mytext+'..'
        elif (i==2):
            mytext = mytext+'...'
        else:
            i=-1
        i+=1
        text_surface = my_font.render(mytext,True,(255,255,255))
        text_surface = pygame.transform.rotate(text_surface,180)
        rect = text_surface.get_rect(center=(160, 120))	
        screen.blit(text_surface,rect)
        
        time.sleep(1)
        pygame.display.flip()
    blue.send(host_IP)
    blue.stop()


def camera_receive(client_IP):
    """
    Requests video feed from a server hosted by the Robot.
    Saves the images in an encoded array
    """
    global code_running
    while code_running:
        try: 
            r= requests.get('http://' + client_IP + ':8000', stream=True,
            timeout=5)
            if(r.status_code == 200):
                bytes1 = bytes()
                global image
                for chunk in r.iter_content(chunk_size=1024):
                    bytes1 += chunk
                    a = bytes1.find(b'\xff\xd8')
                    b = bytes1.find(b'\xff\xd9')
                    if a != -1 and b != -1:
                        jpg = bytes1[a:b+2]
                        bytes1 = bytes1[b+2:]
                        image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 
                        cv2.IMREAD_COLOR)
                        image = np.flip(image, axis=1)
        except Exception as e:
            print("error :{}".format(e))
            time.sleep(1)

h = 0 #global for BNO055 data
r = 0
p = 0

def send_command():
    """
    Sends the BNO055 data to the robot. This function is ran in a thread that
    regularly checks the sensor for data to send. 
    The message is send using UDP socket. The message format is:
    valid:control:heading:roll:pitch

    valid  : if message sent is valid
    control: control enable
    heading: not used 
    roll   : control robot direction
    pitch  : control robot speed and forward/backward movement
    """
    global client_IP, COMMAND_PORT, turn, code_running,h,r,p
    while code_running:
        command_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bno.bno_init()
        try:
            while code_running:
                h,r,p = bno.bno_poll()
                message = str(1)+":"+str(turn)+":"+str(h)+":"+str(r)+":"+str(p)
                command_server.sendto(message.encode(), (client_IP, COMMAND_PORT))
                time.sleep(0.3) #defines the period of when to check and send data
        except Exception as e:
            print("error :{}".format(e))
        command_server.close()

th = threading.Thread(target=camera_receive, args=(client_IP,))
th.setDaemon = True
th.start()

command_thread = threading.Thread(target=send_command)
command_thread.setDaemon = True
command_thread.start()

image = np.zeros((320, 240), dtype=np.uint8)
t = 0
turn_p = turn

while code_running:
	try:
        surf = pygame.Surface((image.shape[0], image.shape[1]))	
        pygame.surfarray.blit_array(surf, image.astype(np.int))
        rect1 = surf.get_rect()
        surf = pygame.transform.rotate(surf, 90)
        rect1.x = 0
        rect1.y = 0
        screen.blit(surf, rect1)
        my_font_hud = pygame.font.Font(None,8)
        my_text_hud = 't:'+str(turn)+' h:'+str(h)+' r:'+str(r)+' p:'+str(p)
        text_surface_hud = my_font.render(my_text_hud,True,(50,255,50))
        text_surface_hud = pygame.transform.rotate(text_surface_hud,180)
        rect = text_surface_hud.get_rect(center=(160, 220))	
        screen.blit(text_surface_hud,rect)	
        if(turn_p != turn):
            
            t = time.time() + 2
            turn_p = turn
            
        if time.time() < t:
            if turn == True:
                my_text = 'Control Enabled!'
            else:
                my_text = 'Control Disabled!'
            text_surface = my_font.render(my_text,True,(255,0,255))
            text_surface = pygame.transform.rotate(text_surface,180)
            rect = text_surface.get_rect(center=(160, 120))		 
            screen.blit(text_surface,rect)
        pygame.display.flip()
	except KeyboardInterrupt:
		code_running = False
		
GPIO.cleanup()
sys.exit(0)
