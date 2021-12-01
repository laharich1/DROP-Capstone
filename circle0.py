import cv2
import numpy as np
# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions


#capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Initialize the camera
camera = PiCamera()

# Set the camera resolution
camera.resolution = (800, 800)

# Set the number of frames per second
camera.framerate = 32

# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(800, 800))

# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)

#while(True):

# Capture frames continuously from the camera
for img in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

  #ret, frame = capture.read()

  #if not (capture.isOpened()):
  #   print("device not found")
    frame = img.array
    rows  = frame.shape[0]
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur  = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                param1=100, param2=39,
                                minRadius=1, maxRadius=50)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            cv2.circle(frame, center, 1, (0, 0, 255), 3)
            radius = i[2]
            cv2.circle(frame, center, radius, (0, 0, 255), 3)

    cv2.imshow('window',frame)
    raw_capture.truncate(0)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
