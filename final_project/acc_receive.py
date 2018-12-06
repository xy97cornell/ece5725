import socket

client_IP = '10.148.0.210'
PORT1 = 5000
BUFFER_SIZE = 1024

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.bind((client_IP, PORT1))
#s1.setblocking(0)
try:
	while True:
		data = s1.recv(BUFFER_SIZE)
		data = data.decode('utf-8')
		print(data)
		#time.sleep(0.5)
except Exception as e:
	print("error :{}".format(e))
	s1.close()
