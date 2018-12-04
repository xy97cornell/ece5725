"""
Bluetooth Client that allows us to to connect and send using
 RFCOMM serial data
"""

from bluedot.btcomm import BluetoothClient, BluetoothAdapter
import time

#device = "B8:27:EB:D7:93:42" #other bluetooth device to pair
device = "7C:B0:C2:AC:16:7D" #Xiaoyu's computer

num = 0

adapter = BluetoothAdapter()
print("Powered = {}".format(adapter.powered))
print(adapter.paired_devices)


def data_recieved(data):
	print(data)

c=BluetoothClient(device,data_recieved, power_up_device=True)



while True:
	
	c.send("hello world, sending data "+str(num))
	num+=1
	time.sleep(1)


