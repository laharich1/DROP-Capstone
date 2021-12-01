import cv2
import numpy as np
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions

# Initialize the camera
camera = PiCamera()

# Set the camera resolution
camera.resolution = (1280, 720)

# Set the number of frames per second
camera.framerate = 32

# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(1280, 720))

# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)

camera.shutter_speed = 1500
size = camera.resolution

t_i = time.time()
video = cv2.VideoWriter(str(t_i)+'.mp4',
						cv2.VideoWriter_fourcc(*'MP4V'),
						5, size)

for img in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    d_t = time.time()-t_i
    frame = img.array
    video.write(frame)
    # cv2.imshow('Frame',frame)


    raw_capture.truncate(0)

    if cv2.waitKey(1) == ord('q') or d_t > 5:
        break

cv2.destroyAllWindows()
