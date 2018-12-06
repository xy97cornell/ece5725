import socket
import tty
import sys
import termios
import subprocess
import re
import time
import threading
import struct
import io
import cv2
import numpy
import requests
from PIL import Image
from bluedot.btcomm import BluetoothServer, BluetoothAdapter

result = subprocess.run('hostname -I', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
host_IP = re.split(' |\n', result)[0]
print("host_IP: "+host_IP)

result = subprocess.run('hcitool dev|grep hci0', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
host_mac = re.split(' |\n|\t', result)[2]
print("host_mac: "+host_mac)

client_IP = '127.0.0.1'

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

COMMAND_PORT=5005
CAM_PORT = 8000
BUFFER_SIZE = 1024
get_ip()
command_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def camera_receive(client_IP):
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
				i = cv2.imencode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
				cv2.imshow('FRAME', i)
				cv2.waitKey(0)

def key_board_poll():
	#keyboard input
	orig_settings = termios.tcgetattr(sys.stdin)
	tty.setraw(sys.stdin)
	x = 0
	while x != chr(27):
		x = sys.stdin.read(1)[0]
		if(x == 'w'):
			message = str(170) + ' ' + str(170)
			command_server.sendto(message.encode(), (client_IP, COMMAND_PORT))
		elif(x == 's'):
			message = str(130) + ' ' + str(130)
			command_server.sendto(message.encode(), (client_IP, COMMAND_PORT))
		elif(x == 'a'):
			message = str(130) + ' ' + str(170)
			command_server.sendto(message.encode(), (client_IP, COMMAND_PORT))
		elif(x == 'd'):
			message = str(170) + ' ' + str(130)
			command_server.sendto(message.encode(), (client_IP, COMMAND_PORT))
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)    


code_running=True;
while code_running:
	
	try:
		
		camera_receive(client_IP)

		
		while True:
			pass
		
	except KeyboardInterrupt:
		code_running = False
		


