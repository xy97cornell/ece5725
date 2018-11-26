import socket
import threading
import bluetooth
import cv2
import numpy as np
import tty
import sys
import termios
import subprocess
import re

result = subprocess.run('hostname -I', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
host_IP = re.split(' |\n', result)[0]
print("host_IP: "+host_IP)

result = subprocess.run('hcitool dev|grep hci0', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
host_mac = re.split(' |\n|\t', result)[2]
print("host_mac: "+host_mac)
#print(host_mac)

def recvImage():
    while True:
        data = s2.recv(BUFFER_SIZE)
        img = np.fromstring(data, np.uint8)
        cv2.imshow('Frame', img)

def get_IP(port=3):
    sbt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print(host_mac)
    sbt.bind((host_mac, 3))
    sbt.listen(1)
    try:
        client, address = sbt.accept()
        print("client_mac: "+address)
        while True:
            message = host_IP + ' ' +  str(5005) + ' ' +  str(5006)
            client.send(bytes(message, 'utf-8'))
            data = client.recv(size)
            data = data.decode('utf-8').split(' ')
            client_IP = data[0]
            print("client_IP: "+client_IP)
            TCP_PORT = data[1]
            print("client_TCP_PORT: "+TCP_PORT)
            UDP_PORT = data[2]
            print("client_UDP_PORT: "+UDP_PORT)
            return
    except:
        client.close()
        sbt.close()

client_IP = '127.0.0.1'
TCP_PORT = 5005
UDP_PORT = 5006
BUFFER_SIZE = 1024
get_IP()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host_IP, TCP_PORT))
s.listen(1)
client, addr = s.accept()
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2.bind((host_IP, UDP_PORT))
s2.setblocking(0)
threading.Thread(target=recvImage).start()

#keyboard input
orig_settings = termios.tcgetattr(sys.stdin)
tty.setraw(sys.stdin)
x = 0
while x != chr(27):
    x = sys.stdin.read(1)[0]
    if(x == 'w'):
        message = str(170) + ' ' + str(170)
        client.send(message)
    elif(x == 's'):
        message = str(130) + ' ' + str(130)
        client.send(message)
    elif(x == 'q'):
        message = str(130) + ' ' + str(170)
        client.send(message)
    elif(x == 'e'):
        message = str(170) + ' ' + str(130)
        client.send(message)
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)    
