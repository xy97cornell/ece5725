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
import accelerometer
import RPi.GPIO as GPIO

result = subprocess.run('hostname -I', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
host_IP = re.split(' |\n', result)[0]
print("host_IP: "+host_IP)

result = subprocess.run('hcitool dev|grep hci0', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
host_mac = re.split(' |\n|\t', result)[2]
print("host_mac: "+host_mac)

client_IP = '10.148.4.162'

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
turn = 0

def GPIO22_callback(channel):
    """
    interrupt handler for GPIO17; button on piTFT
    """
    print ("in interrupt 22")
    global turn 
    turn = 1 if 0 else 1
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)


def data_recieved(data):
	global client_IP
	global flag
	global blue
	print("Got IP from Client! IP: "+ str(data))
	client_IP = data
	flag = False

def get_ip():
	global flag
	blue =  BluetoothServer(data_recieved, power_up_device=True)
	flag = True
	while flag:
		time.sleep(1)
	blue.send(host_IP)
	blue.stop()

COMMAND_PORT=5000
CAM_PORT = 8000
BUFFER_SIZE = 1024
get_ip()
time.sleep(2)

def camera_receive(client_IP):
	while True:
		try: 
			r= requests.get('http://' + client_IP + ':8000', stream=True)
			if(r.status_code == 200):
				bytes1 = bytes()
				for chunk in r.iter_content(chunk_size=1024):
					bytes1 += chunk
					a = bytes1.find(b'\xff\xd8')
					b = bytes1.find(b'\xff\xd9')
					if a != -1 and b != -1:
						jpg = bytes1[a:b+2]
						bytes1 = bytes1[b+2:]
						i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
						cv2.imshow('FRAME', i)
						cv2.waitKey(1)
		except Exception as e:
			print("error :{}".format(e))
			time.sleep(1)


def send_command():
	global client_IP, COMMAND_PORT, turn
	while True:
		command_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		accelerometer.bno_init()
		try:
			while True:
				h,r,p = accelerometer.bno_poll()
				print ("r = ",r)
				message = str(1)+":"+str(turn)+":"+str(h)+":"+str(r)+":"+str(p)
				command_server.sendto(message.encode(), (client_IP, COMMAND_PORT))
				time.sleep(0.3)
				
		except Exception as e:
			print("error :{}".format(e))
			
		command_server.close()

th = threading.Thread(target=camera_receive, args=(client_IP,))
th.setDaemon = True
th.start()

command_thread = threading.Thread(target=send_command)
command_thread.setDaemon = True
command_thread.start()
#camera_receive(client_IP)
code_running=True;
while code_running:
	
	try:
		time.sleep(1)
	
	except KeyboardInterrupt:
		code_running = False
		


