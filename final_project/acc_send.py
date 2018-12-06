import accelerometer
import time
import socket

client_IP = '10.148.0.210'
PORT1 = 5000

code_running = True
if __name__=='__main__':
	while code_running:
		command_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		accelerometer.bno_init()
		try:
			while True:
				h,r,p = accelerometer.bno_poll()
				print ("r = ",r)
				message = str(h)+":"+str(r)+":"+str(p)
				command_server.sendto(message.encode(), (client_IP, PORT1))
				time.sleep(0.9)
				
		except Exception as e:
			print("error :{}".format(e))
			
		command_server.close()
			
