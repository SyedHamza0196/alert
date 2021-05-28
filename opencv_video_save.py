import cv2
import numpy as np
from datetime import datetime,date
import time
import configparser

start_time = time.time()
config = configparser.ConfigParser()
config.read("./config.yaml")

rtsp = config['rtsp']['link']
recording_ending_time = config['time']['recording_ending_time']

current_time = datetime.now().strftime("%H%M%S")
current_date = date.today().strftime("%d%m%Y")

cap = cv2.VideoCapture(rtsp)

if (cap.isOpened() == False): 
  print("Unable to read camera feed")

frame_width = int(cap.get(3))#1920
frame_height = int(cap.get(4))#1080

out = cv2.VideoWriter(current_time+'_'+current_date+'.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

while(True):
    ret, frame = cap.read()
    
    if ret == True and int(time.time()-start_time) == recording_ending_time:
        out.write(frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    else:
        break