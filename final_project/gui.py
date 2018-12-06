import RPi.GPIO as GPIO
import pygame
os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 
os.putenv('SDL_MOUSEDRV', 'TSLIB') #setup mouse in pygame
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen') #touchscreen as mouse
pygame.init()
pygame.mouse.set_visible(False)

def GPIO22_callback(channel):
    print "in interrupt 22"
    global enable1
    enable = not enable

def GPIO23_callback(channel):
    print "in interrupt 23"
    global #sock
    #sock.send((0,0,90))
    
def GPIO27_callback(channel):
    print "in interrupt 23"
    global #sock
    #sock.send((0,90,0))

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
GPIO.add_event_detect(22,GPIO.FALLING,callback=GPIO22_callback,bouncetime=300)
GPIO.add_event_detect(23,GPIO.FALLING,callback=GPIO23_callback,bouncetime=300)
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO23_callback,bouncetime=300)
screen = pygame.display.set_mode(size)
pygame.init()

image = np.zeros((320, 240), dtype=np.uint8)
code_running=True;
my_font = pygame.font.Font(None,50)
t = 0
while code_running:
    surf = pg.Surface((image.shape[0], image.shape[1]))
    # draw the array onto the surface
    pygame.surfarray.blit_array(surf, image)
    if(enable_p != enable)
        t = time.time() + 2
        enable_p = enable
        
    if time.time() < t:
        if enable == True:
            my_text = 'Sensor enabled!'
        else:
            my_text = 'Sensor disabled!'
        text_surface = my_font.render(my_text,True,(255,255,255))
        rect = text_surface.get_rect(center=(160, 120))
        screen.blit(text_surface,rect)
    

    # First level buttons

    
def camera_receive(client_IP):
	while True:
		try: 
			r= requests.get('http://' + client_IP + ':8000', stream=True)
			if(r.status_code == 200):
				bytes1 = bytes()
                global image
				for chunk in r.iter_content(chunk_size=1024):
					bytes1 += chunk
					a = bytes1.find(b'\xff\xd8')
					b = bytes1.find(b'\xff\xd9')
					if a != -1 and b != -1:
						jpg = bytes1[a:b+2]
						bytes1 = bytes1[b+2:]
						image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        res = cv2.resize(img, dsize=(320, 240), interpolation=cv2.INTER_CUBIC)
		except Exception as e:
			print("error :{}".format(e))
			time.sleep(1)
