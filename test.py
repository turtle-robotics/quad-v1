#!/usr/bin/python3

import atexit
import socket
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (1280, 720)})
picam2.configure(video_config)
encoder = H264Encoder(1000000)

atexit.register(picam2.stop_recording)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect(("framework.local", 10001))
    stream = sock.makefile("wb")
    picam2.start_recording(encoder, FileOutput(stream))
    while True:
        time.sleep(20)
