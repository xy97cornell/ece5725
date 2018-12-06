import RPi.GPIO as GPIO
import pygame
os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 
os.putenv('SDL_MOUSEDRV', 'TSLIB') #setup mouse in pygame
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen') #touchscreen as mouse
pygame.init()
pygame.mouse.set_visible(False)

def GPIO17_callback(channel):
    """Bail out button interrupt"""
    print "in interrupt 17"
    global code_running
    code_running = False

code_running=True;
while code_running:
	
	try:
		camera_receive(client_IP)
        
		
		while True:
			pass
		
	except KeyboardInterrupt:
		code_running = False

def camera_receive(client_IP):
	r= requests.get('http://' + client_IP + ':8000', stream=True)
	if(r.status_code == 200):
		bytes1 = bytes()
		for chunk in r.iter_content(chunk_size=1024):
			bytes1 += chunk
			a = bytes1.find(b'\xff\xd8')
			b = bytes1.find(b'\xff\xd9')
			if a != -1 and b != -1:
				jpg = bytes1[a:b+2]
				bytes1 = bytes1[b+2:]
				i = cv2.imencode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
				cv2.imshow('FRAME', i)
				cv2.waitKey(1)
