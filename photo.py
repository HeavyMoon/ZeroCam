#!/usr/bin/env python3
#######################################
# capture image
#######################################
import logging
import os
import time

from picamera2 import Picamera2

# log for terminal
log_msg_format  = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
log_date_format = "%Y/%m/%d %H:%M:%S"
logging.basicConfig(format=log_msg_format, datefmt=log_date_format, level=logging.INFO)
logger = logging.getLogger("capture")

def photo():
    logger.info(f"open picam")
    picam = Picamera2()
    capture_config = picam.create_still_configuration(raw={}, display=None)

    picam.start()
    time.sleep(0.3)

    logger.info("capture and save")
    img = picam.switch_mode_capture_request_and_stop(capture_config)
    script_path = os.path.dirname(__file__)
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    img.save("main",f"{script_path}/photo/{timestamp}.jpg")
    img.save_dng(f"{script_path}/photo/{timestamp}.dng")

    picam.close()

if __name__ == "__main__":
    photo()

