from cfgreader import config as config
import time
from queue import Queue
from threading import Thread
import redis
from datetime import datetime
import cv2
import numpy as np
from datetime import datetime,date
import time
import proto.Inference_pb2 as inference
import logging as logger

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
      classD = config.detectionClassid_for_recording
      labelD = config.detectionLabel_for_recording
      if bound.label == labelD or bound.classid == classD:
        start_time = time.time()
        current_time = datetime.now().strftime("%H%M%S")
        current_date = date.today().strftime("%d%m%Y")
        rtsp = config.rtsp_for_recording
        
        cap = cv2.VideoCapture(rtsp) #rtsp

        if (cap.isOpened() == False): 
          logger.error("Unable to read camera feed")

        frame_width = int(cap.get(3))#1920
        frame_height = int(cap.get(4))#1080
        rType = config.recording_type

        out = cv2.VideoWriter(current_time+'_'+current_date+rType,cv2.VideoWriter_fourcc('M','J','P','G'), 25, (frame_width,frame_height))

        while(True):
            ret, frame = cap.read()
            
            if ret == True and int(time.time()-start_time) == 3600: # and int(time.time()-start_time) == recording_ending_time
                out.write(frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
            else:
                break
      
def main():
  run(redis.Redis(host=config.redis_host, port=config.redis_port, db=0))

if __name__ == '__main__': 
    main()