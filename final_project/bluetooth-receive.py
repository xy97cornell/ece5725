"""
Bluetooth Server that allows us to to connect and accept
incoming RFCOMM serial data
"""

from bluedot.btcomm import BluetoothClient
from time import time

device = "B8:27:EB:D7:93:42" #rpi2 bluetooth device to pair
#device = "7C:B0:C2:AC:16:7D" #Xiaoyu's computer

adapter = BluetoothAdapter()
print("Powered = {}".format(adapter.powered))
print(adapter.paired_devices)


def data_recieved(data):
	print(data)
	
	c.send("received " + str(num))
	num+=1

c=BluetoothClient(device,data_recieved, power_up_device=True)
num = 0

	
while True:
	
	sleep(1)


