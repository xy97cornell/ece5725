import RPi.GPIO as GPIO
import socket
import threading
import bluetooth
import cv2
import numpy as np
import picamera
import subprocess
import re
import time
from bluedot.btcomm import BluetoothClient, BluetoothAdapter
import io
import struct

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
p1 = GPIO.PWM(6, 100000/2150)
p2 = GPIO.PWM(13, 100000/2150)
p1.start(150/2150.0*100)
p2.start(150/2150.0*100)

result = subprocess.run('hostname -I', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
client_IP = re.split(' |\n', result)[0]
print("client_IP: "+client_IP)

class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)

def set_speed(interval1, interval2):
    p1.ChangeDutyCycle(interval1/(2000.0+interval1)*100)
    p1.ChangeFrequency(100000/(2000.0+interval1))
    p2.ChangeDutyCycle(interval2/(2000.0+interval2)*100)
    p2.ChangeFrequency(100000/(2000.0+interval2))

def data_recieved(data):
    global host_IP
    global flag
    print(data)
    host_IP = data
    flag = False
    
def sendIP():
	global flag
	flag = True
	c = BluetoothClient('B8:27:EB:2A:46:91', data_recieved, power_up_device=True)
	while flag:
		c.send(client_IP)
		time.sleep(1)
	c.disconnect()

def stream(sock, connection):
	while(True)
		try:
			output = SplitFrames(connection)
			with picamera.PiCamera(resolution=(320,240), framerate=15) as camera:
				time.sleep(2)
				start = time.time()
				camera.start_recording(output, format='jpeg', quality = 10)
				print("camera_start")
				camera.wait_recording(20)
				camera.stop_recording()
				# Write the terminating 0-length to the connection to let the
				# server know we're done
				#connection.write(struct.pack('<L', 0))
		except socket.error:
			s2.connect((host_IP, 8000))
			connection = s2.makefile('wb')
			continue
		finally:
			#connection.close()
			#sock.close()
			finish = time.time()
		#print('Sent %d images in %d seconds at %.2ffps' % (
			#output.count, finish-start, output.count / (finish-start)))

PORT1 = 5005
BUFFER_SIZE = 1024
connected = True
run = True
sendIP()
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.bind((client_IP, PORT1))
s1.setblocking(0)
time.sleep(1)
s2 = socket.socket()
s2.connect((host_IP, 8000))
connection = s2.makefile('wb')
streamer = threading.Thread(target = stream, args = (s2, connection,))
streamer.daemon = True
streamer.start()

t = 0
while run:
	try:
		while True:
			try:
				data = s1.recv(BUFFER_SIZE)
				print(data)
				data = data.decode('utf-8').split(' ')
				set_speed(int(data[0]), int(data[1]))
				t = time.time()
			except BlockingIOError:
				if time.time() > t+0.2:
					set_speed(150, 150)
					if not connected:
						break
						continue
	except KeyboardInterrupt:
		run = False

	

	
