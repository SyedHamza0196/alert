from cfgreader import config as config
from PIL import Image
import time
import redis
from datetime import datetime
import cv2
import numpy as np
from datetime import datetime,date
import time
import proto.Inference_pb2 as inference
import logging as logger
from imageio import imread
import io
import base64
from queue import Queue
from threading import Thread

def run(client):
  while(1):
    #------------------ redis ------------------------------------
    timestamp = client.blpop(config.recorder_in_channel.encode(), 0)[1]
    if timestamp is None:
        time.sleep(0.05)
        continue
    #get data wrt timestamp from tracker_in_channel or DetectorOutQueue
    track_data = client.hget(timestamp, b'InferResults') 
    if track_data is None:
        time.sleep(0.05)
        continue
    track_result = inference.DetectorResults()
    track_result.ParseFromString(track_data)
    #put data back wrt timestamp in tracker_in_channel or DetectorOutQueue
    out=track_result.SerializeToString()
    client.hset(timestamp,b'InferResults',out)
    client.pexpire(timestamp,config.redis_hash_timeout)
    client.rpush(config.recorder_out_channel,timestamp)
    client.ltrim(config.recorder_out_channel,-4,-1)
    #------------------ redis ------------------------------------
    
    for i, bound in enumerate(track_result.bounds):
      # classD = config.Classid_for_recording
      # labelD = config.Label_for_recording
      if bound.label == config.Label_for_recording or bound.classid == config.Classid_for_recording:
        start_time = time.time()
        current_time = datetime.now().strftime("%H%M%S")
        current_date = date.today().strftime("%d%m%Y")
        
        # img BGR
        img = cv2.imdecode(np.frombuffer(track_result.frame.mat_data, np.uint8), cv2.IMREAD_COLOR)
        # covert BRG to RGB
        img_np = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        #numpy to Image
        img_showable = Image.fromarray(img_np)
        # frame = imread(io.BytesIO(base64.b64decode(track_result.frame.mat_data.decode())))
        
        # frame_width = int(cap.get(3))#1920
        # frame_height = int(cap.get(4))#1080
        # rType = config.recording_type
        out = cv2.VideoWriter(current_time+'_'+current_date+config.recording_type,cv2.VideoWriter_fourcc(*'XVID'), 25, (img_showable.shape[1],img_showable.shape[0])) #'M','J','P','G'   #*'XVID' #*'MPEG'
        out.write(img_showable)
      
def main():
  run(redis.Redis(host=config.redis_host, port=config.redis_port, db=0))

if __name__ == '__main__': 
    main()