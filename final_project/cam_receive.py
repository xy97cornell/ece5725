import io
import socket
import struct
import cv2
import numpy
from PIL import Image

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('10.148.0.210', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    #video = cv2.VideoCapture('tcp://192.168.137.246:8000/')
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        #print(type(image).__name__)
        image = numpy.array(image).astype(numpy.uint8)
        #print(image.shape)
        #print('!!!')
        #ret, image = video.read()
        #print(image.shape)
        cv2.imshow('frame', image)
        cv2.waitKey(1)
        #cv2.imshow('frame', i
        #sleep(0.2)
finally:
  
    connection.close()
    server_socket.close()
