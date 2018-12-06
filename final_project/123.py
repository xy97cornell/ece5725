from PIL import Image
import requests
from io import BytesIO
import cv2
import numpy as np

r= requests.get("http://10.148.4.162:8000", stream=True)
if(r.status_code == 200):
    bytes = bytes()
    for chunk in r.iter_content(chunk_size=1024):
        bytes += chunk
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('i', i)
            cv2.waitKey(0)
