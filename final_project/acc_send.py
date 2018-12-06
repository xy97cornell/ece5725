import accelerometer
import time
import socket
import RPi.GPIO as GPIO

client_IP = '10.148.0.210'
PORT1 = 5000

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
turn = 0

def GPIO22_callback(channel):
    """
    interrupt handler for GPIO17; button on piTFT
    """
    print ("in interrupt 22")
    global turn 
    turn = 1 if 0 else 1


GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)

code_running = True
if __name__=='__main__':
	while code_running:
		command_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		accelerometer.bno_init()
		try:
			while True:
				h,r,p = accelerometer.bno_poll()
				print ("r = ",r)
				message = str(1)+":"+str(turn)+":"+str(h)+":"+str(r)+":"+str(p)
				command_server.sendto(message.encode(), (client_IP, PORT1))
				time.sleep(0.9)
				
		except Exception as e:
			print("error :{}".format(e))
			
		command_server.close()
			
