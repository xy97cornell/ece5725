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

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
p1 = GPIO.PWM(6, 100000/2150)
p2 = GPIO.PWM(13, 100000/2150)
p1.start(150/2150.0*100)
p2.start(150/2150.0*100)
camera = picamera.PiCamera()
camera.resolution = (256, 320)
camera.framerate = 24
global img
img = np.zeros((320, 256, 3), dtype=np.uint8)
global img0
img0 = np.zeros((320, 256, 3), dtype=np.uint8)

result = subprocess.run('hostname -I', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
client_IP = re.split(' |\n', result)[0]
print("client_IP: "+client_IP)
global n
n = 0
def sendImage():
    global img
    global img0
    global connection
    n = 0
    while True:
        #threading.Timer(0.5, sendImage).start() 
        camera.capture(img, 'rgb')
        #cv2.imshow('frame',img)
        #cv2.waitKey(25)
        diff = (img.astype(np.int16) - img0.astype(np.int16))/2
        diff = diff.astype(np.int8).view(np.uint8)
        diff += 128
        if n % 5 == 0:
            compressed = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 40])[1].tostring()
            #print(np.fromstring(compressed,np.uint8).shape)
            #img = cv2.imdecode(np.fromstring(compressed, np.uint8), cv2.IMREAD_COLOR)
            #cv2.imshow('frame', img)
            #cv2.waitKey()
        else:
            compressed = cv2.imencode('.jpg', diff, [cv2.IMWRITE_JPEG_QUALITY, 60])[1].tostring()
        l = len(compressed)
        #print(compressed)
        i = 0
        print(1, time.time())
        try:
            while i < l:
                ma = min(i+1024, l)
                s2.send(compressed[i:ma])
                i = i + 1024
            if n % 5 == 0:
                s2.send(b'NEW')
            else:
                s2.send(b'BYE')
        except socket.error:
            connection = False
        print(2, time.time())
        img0 = np.copy(img)
        n = n + 1
        #time.sleep()
	
def set_speed(interval1, interval2):
    p1.ChangeDutyCycle(interval1/(2000.0+interval1)*100)
    p1.ChangeFrequency(100000/(2000.0+interval1))
    p2.ChangeDutyCycle(interval2/(2000.0+interval2)*100)
    p2.ChangeFrequency(100000/(2000.0+interval2))
'''
def get_IP(host_mac, port=5):
    sbt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sbt.connect((host_mac, port))
    while true:
        data = sbt.recv(1024)
        data = data.decode('utf-8').split(' ')
        host_IP = data[0]
        TCP_PORT = data[1]
        UDP_PORT = data[2]
        print("host_IP: "+host_IP)
        message = client_IP + ' ' +  str(5005) + ' ' +  str(5006)
        sbt.send(bytes(message, 'utf-8'))
        return
'''

host_IP = '10.148.0.46'
PORT1 = 5005
PORT2 = 5008
BUFFER_SIZE = 1024
host_mac = '88:B1:11:67:6E:A1'
connectin = False

run = True
while run:
    try:
        if not connectin:
            print ("Starting connection")
            s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s1.bind((client_IP, PORT1))
            s1.setblocking(0)
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect((host_IP, PORT2))
            th = threading.Thread(target=sendImage)
            th.daemon = True
            th.start()
            t = time.time()
            connectin = True
            
        while True:
            try:
                data = s1.recv(BUFFER_SIZE)
                data = data.decode('utf-8').split(' ')
                set_speed(int(data[0]), int(data[1]))
                t = time.time()
            except BlockingIOError:
                if time.time() > t+0.2:
                    set_speed(150, 150)
                    if not connectin:
                        break
                continue
    except KeyboardInterrupt:
        run = False
    except:
        connectin = False
	

	
