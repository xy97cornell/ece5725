# client.py
# 12/7/2018 
# Xiaoyu Yan (xy97) and Ji Wu (jw2473)
# Final Project - Telepresence Vehicle
#
# Main control file for robot. Sends its IP address to the basestation 
# and gets basestation IP address.
# Receives and decodes commands from basestation and sets up a host 
# server for the camera stream
# Handles servo movements to control robot movement 
#


import RPi.GPIO as GPIO
import socket
import threading
import cv2
import numpy as np
import picamera
import subprocess
import re
import time
from bluedot.btcomm import BluetoothClient, BluetoothAdapter
import io
import struct
import socketserver
from http import server
from threading import Condition
import Robot #custom library

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
p1 = GPIO.PWM(6, 100000/2150)
p2 = GPIO.PWM(13, 100000/2150)
p1.start(150/2150.0*100)
p2.start(150/2150.0*100)

## Get IP address
result = subprocess.run('hostname -I', stdout=subprocess.PIPE, 
shell=True)
result = result.stdout.decode('utf-8')
client_IP = re.split(' |\n', result)[0]
print("client_IP: "+client_IP)


PORT1 = 5000
BUFFER_SIZE = 1024
connected = True
run = True
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
    """
    Streaming video to HTTP server
    """
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 
            'multipart/x-mixed-replace; boundary=FRAME')
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



def data_received(data):
    """
    Callback function for bluetooth data received 
    """
    global host_IP
    global flag
    print('host_IP: ' + data)
    host_IP = data
    flag = False
    
def sendIP():
    """
    Repeatedly sends the string containing IP address to target. 
    Requires the MAC address of the target to be hardcoded.
    Receives back IP address from target and saves it for UDP 
    connection
    Blocks until we connect with base station 
    """
    global flag
    flag = True
    c = BluetoothClient('B8:27:EB:2A:46:91', data_received, 
    power_up_device=True)
    while flag:
        c.send(client_IP)
        time.sleep(1)
    c.disconnect()

sendIP()
### Connection good!! Start everything else
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.bind((client_IP, PORT1))
s1.setblocking(0)

camera = picamera.PiCamera(resolution=(320, 240), framerate=24)
output = StreamingOutput()
camera.start_recording(output, format='mjpeg')
address = ('', 8000)
server = StreamingServer(address, StreamingHandler)

def func(server):
    """
    Threading function for hosting camera stream
    """
    server.serve_forever()


thread = threading.Thread(target=func, args=(server,))
thread.setDaemon = True
thread.start()

robot = Robot.Robot()
t = 0
while run:
    try:
        data = s1.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
        robot.command(data)
        print(data)
        t = time.time() + 1
        
    except BlockingIOError:
        data = "0:0:0:0:0" #sends invalid data to stop robot
        if time.time()>t:
            robot.command(data) 

        


	

	
