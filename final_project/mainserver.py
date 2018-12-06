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
import traceback
            
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
cam_server = socket.socket()
cam_server.bind((host_IP, CAM_PORT))
cam_server.listen(0)
# Accept a single connection and make a file-like object out of it
cam_connection = cam_server.accept()[0]
#cam_connection.settimeout(20)
connection = cam_connection.makefile('rb')
def camera_receive(sock, connection):
	try:
		#video = cv2.VideoCapture('tcp://192.168.137.246:8000/')
		'''
		cmdline = ['mplayer', '-fps', '25', '-cache', '128', '-']
		player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
		'''
		while True:
			'''
			try:
				data = connection.read(1024)
				print("!!!")
				if not data:
					break
				player.stdin.write(data)
			except socket.error:
				cam_connection = cam_server.accept()[0].makefile('rb')
				continue
			'''
			# Read the length of the image as a 32-bit unsigned int. If the
			# length is zero, quit the loop
			image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
			if not image_len:
				break
			# Construct a stream to hold the image data and read the image
			# data from the connection
			image_stream = io.BytesIO()
			image_stream.write(connection.read(image_len))
			# Rewind the stream, open it as an image with PIL and do some
			# processing on it
			
			image_stream.seek(0)
			image = Image.open(image_stream)
		
			
			image = numpy.array(image).astype(numpy.uint8)
			cv2.imshow('frame', image)
			cv2.waitKey(1)
			
	except:
		print('disconnected')
		sock.listen(0)
		cam_connection = sock.accept()[0]
		cam_connection.settimeout(20)
		connection = cam_connection.makefile('rb')
		
	finally:
		connection.close()
		sock.close()

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
		
		camera = threading.Thread(target=camera_receive, args=(cam_server,connection))
		camera.daemon = True
		camera.start()
		
		while True:
			pass
		
	except KeyboardInterrupt:
		traceback.print_exc()
		code_running = False
		


