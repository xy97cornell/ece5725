"""
Bluetooth Server that allows us to to connect and accept
incoming RFCOMM serial data
"""

from bluedot.btcomm import BluetoothServer, BluetoothAdapter
import time
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


adapter = BluetoothAdapter()
print("Powered = {}".format(adapter.powered))
print(adapter.paired_devices)
num = 0
Connection = True
conn=True

def data_recieved(data):
	global num,conn
	print("received data #"+str(num))
	print(data)
	c.send(host_IP)
	num+=1
	conn=True

c=BluetoothServer(data_recieved, power_up_device=True)
while Connection:
	if(c.client_connected and conn):
		print("connection from: "+str(c.client_address))
		conn=False
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		print("disconnected by keyboard")
		Connection=False


