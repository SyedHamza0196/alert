import cv2
import numpy as np
from PIL import Image

img = cv2.imread('/home/hamza/Pictures/test.png')
img_str = cv2.imencode('.jpg', img)[1].tostring()

print("saveable format")
# print(img_str)

# img BGR
img = cv2.imdecode(np.frombuffer(img_str, np.uint8), cv2.IMREAD_COLOR)
# covert BRG to RGB
img_np = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
#numpy to Image
img_showable = Image.fromarray(img_np)

# nparr = np.fromstring(img_str, np.uint8)
# print(nparr)
# img_showable = cv2.imdecode(nparr, cv2.imread)

print("showable format")
print(type(img_showable))