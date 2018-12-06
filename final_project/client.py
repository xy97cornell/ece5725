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
import traceback
import socketserver
from http import server
from threading import Condition

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

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                pass


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def set_speed(interval1, interval2):
    p1.ChangeDutyCycle(interval1/(2000.0+interval1)*100)
    p1.ChangeFrequency(100000/(2000.0+interval1))
    p2.ChangeDutyCycle(interval2/(2000.0+interval2)*100)
    p2.ChangeFrequency(100000/(2000.0+interval2))

def data_recieved(data):
    global host_IP
    global flag
    print('host_IP: ' + data)
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



PORT1 = 5005
BUFFER_SIZE = 1024
connected = True
run = True
sendIP()
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.bind((client_IP, PORT1))
s1.setblocking(0)

camera = picamera.PiCamera(resolution='640x480', framerate=24)
output = StreamingOutput()
camera.start_recording(output, format='mjpeg')
address = ('', 8000)
server = StreamingServer(address, StreamingHandler)
thread = threading.Thread(server.serve_forever())
thread.setDaemon = True
thread.start()


t = 0
while run:
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


	

	
