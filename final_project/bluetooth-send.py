"""
Bluetooth Client that allows us to to connect and send using
 RFCOMM serial data
"""
import subprocess
from bluedot.btcomm import BluetoothClient, BluetoothAdapter
import time
import re

device = "B8:27:EB:2A:46:91" #other bluetooth device to pair
#device = "7C:B0:C2:AC:16:7D" #Xiaoyu's computer

result = subprocess.run('hostname -I', stdout=subprocess.PIPE, shell=True)
result = result.stdout.decode('utf-8')
client_IP = re.split(' |\n', result)[0]

print("client_IP: "+client_IP)
num = 0

adapter = BluetoothAdapter()
print("Powered = {}".format(adapter.powered))
print(adapter.paired_devices)



def data_recieved(data):
    global host_IP
    global flag
    host_IP = data
    flag = False

flag = True
c = BluetoothClient(device, data_recieved, power_up_device=True)

while flag:
    c.send(client_IP)
    time.sleep(1)

c.disconnect

