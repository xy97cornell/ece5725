import socket
import subprocess
import re
import time
import threading
import struct
import io
import cv2
import numpy
import RPi.GPIO as GPIO
import os
from PIL import Image
from bluedot.btcomm import BluetoothServer, BluetoothAdapter

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/dv1')

COMMAND_PORT=5005
CAM_PORT = 8000
BUFFER_SIZE = 1024


result = subprocess.run('hostname -I', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
host_IP = re.split(' |\n', result)[0]
print("host_IP: "+host_IP)

result = subprocess.run('hcitool dev|grep hci0', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
host_mac = re.split(' |\n|\t', result)[2]
print("host_mac: "+host_mac)


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
buttonPressed = False
command = 0

def GPIO17_callback(channel):
    """
    interrupt handler for GPIO17; button on piTFT
    """
    print ("in interrupt 17")
    global buttonPressed, command
    buttonPressed = True
    command = 17


def GPIO22_callback(channel):
    """
    interrupt handler for GPIO22; button on piTFT
    """
    print ("in interrupt 22")
    global buttonPressed, command
    buttonPressed = True
    command = 22


def GPIO23_callback(channel):
    """
    interrupt handler for GPIO23; button on piTFT
    """
    print ("in interrupt 23")
    global buttonPressed, command
    buttonPressed = True
    command = 23


def GPIO27_callback(channel):
    """
    interrupt handler for GPIO27; button on piTFT
    """
    print ("in interrupt 27")
    global buttonPressed, command
    buttonPressed = True
    command = 27


GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)

client_IP = '127.0.0.1'

def data_recieved(data):
	global client_IP
	global flag
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


get_ip()
command_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cam_server = socket.socket()
cam_server.bind((host_IP, CAM_PORT))
cam_server.listen(0)
# Accept a single connection and make a file-like object out of it
cam_connection = cam_server.accept()[0].makefile('rb')

def camera_receive(socket, connection):
	try:
		#video = cv2.VideoCapture('tcp://192.168.137.246:8000/')
		while True:
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
	finally:
		connection.close()      
		socket.close()

def button_send(socket):
    global buttonPressed, command
    try:
        while True:
            if (buttonPressed):
                buttonPressed = False
                socket.sendto(str(command).encode(), (client_IP, COMMAND_PORT))

    finally:
        socket.close()

code_running=True
camera = threading.Thread(target=camera_receive, args=(cam_server,cam_connection))
camera.daemon = True
camera.start()
button = threading.Thread(target=button_send, args=(command_server,))
button.daemon = True
button.start()

while code_running:
    try:
        time.sleep(0.5)
    except KeyboardInterrupt:
        print ("keyboard interrupt")
        code_running = False
        command_server.close()
        cam_server.close()
        GPIO.cleanup()
		
		


