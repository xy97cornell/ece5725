from picamera import PiCamera
from time import sleep

# only works if pi connected to monitor

# camera.capture('/home/pi/Desktop/image.jpg') #captures a still image
# Important to sleep for at least 2 seconds to give time for 
# camera to adjust to environment

# Camera video
# camera.start_preview()
# camera.start_recording('/home/pi/video.h264')
# sleep(10)
# camera.stop_recording()
# camera.stop_preview()
# type omxplayer video.h264

# camera settings
# camera.resolution = (2592, 1944) # max for images
# videos have max resolution of 1920 x 1080
# minumum is 64 x 64
# camera.framerate = 15

# Settings
# camera.annotate_text = "Hello world!""
# camera.brightness = 70
# camera.rotation = 180 #90, 180, 270
# camera.start_preview(alpha=200) #change alpha level and transparency
# camera.contrast

camera = PiCamera()

camera.start_preview()
sleep(10)
camera.stop_preview()