#!/usr/bin/env python3
#######################################
# capture video
#######################################
import logging
import os
import time

from picamera2.encoders import H264Encoder
from picamera2 import Picamera2

# log for terminal
log_msg_format  = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
log_date_format = "%Y/%m/%d %H:%M:%S"
logging.basicConfig(format=log_msg_format, datefmt=log_date_format, level=logging.INFO)
logger = logging.getLogger("capture")

def video(sec:int):
    logger.info(f"open picam")
    picam = Picamera2()
    video_config = picam.create_video_configuration()
    picam.configure(video_config)
    encoder = H264Encoder(bitrate=10000000)

    script_path = os.path.dirname(__file__)
    timestamp = time.strftime('%Y%m%d_%H%M%S')

    logger.info("capture and save")
    picam.start_recording(encoder, f'{script_path}/video/{timestamp}.h264')
    time.sleep(sec)
    picam.stop_recording()

    picam.close()

if __name__ == "__main__":
    video(5)

