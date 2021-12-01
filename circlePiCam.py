import cv2
import numpy as np
# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
from image_util import *
from vectorization import send_angle_r


#capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Initialize the camera
camera = PiCamera(0)


# Set the camera resolution
camera.resolution = (1280, 720)

# Set the number of frames per second
camera.framerate = 32

prev_loc = None

# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(1280, 720))

# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)

camera.shutter_speed = 1500
# camera.iso = 2000
notfound = 0
found = 0

# print(camera.iso, camera.shutter_speed, camera.exposure_speed)

#while(True):
t_i = time.time()

# Capture frames continuously from the camera
# while(True):
for img in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

    # ret, frame = camera.read()

    # if not (camera.isOpened()):
    #     print("device not found")

    # print("Total frames so far:", found + notfound)
    frame = img.array
    rows = frame.shape[0]
    cols = frame.shape[1]
    #img_center = (cols//2 - 45, rows//2 + 95)
    img_center = (cols//2, rows//2)

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur  = cv2.medianBlur(gray, 5)
    #Original threashhold was 150
    ret, thr = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(thr, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                param1=100, param2=35,
                                minRadius=1, maxRadius=100)

    thr2 = np.zeros_like(frame)
    thr2[:,:,0] = thr
    thr2[:,:,1] = thr
    thr2[:,:,2] = thr

    if circles is not None:
        found += 1
        circles = np.uint16(np.around(circles))
        target_center, target_radius = chooseCircle(circles, prev_loc, img_center)
        prev_loc = target_center

        for i in circles[0, :]:
            center = (i[0], i[1])
            cv2.circle(frame, center, 1, (0, 0, 255), 3)
            radius = i[2]
            cv2.circle(frame, center, radius, (0, 0, 255), 3)

            cv2.circle(thr2, center, 1, (0, 0, 255), 3)
            cv2.circle(thr2, center, radius, (0, 0, 255), 3)

    else:
        target_center = prev_loc
        notfound += 1

    if target_center != None:

        top_left = (target_center[0]-target_radius, target_center[1]-target_radius)
        bot_right = (target_center[0]+target_radius, target_center[1]+target_radius)
        cv2.rectangle(frame, top_left, bot_right, (255, 0, 0), 3)

        start = img_center
        end = target_center
        # print(target_center)
        cv2.line(frame, start, end, (0,255,0), 2)
        dist, angleR = relativeLocation(target_center, img_center)
        print('frame', (found+notfound), ':', np.round(np.degrees(angleR), 1), 'deg')
        # send_angle_r(angleR, dist)


        cv2.rectangle(thr2, top_left, bot_right, (255, 0, 0), 3)

    r_dim = (cols//2, rows//2)
    stitch = np.concatenate((cv2.resize(frame,r_dim), cv2.resize(thr2,r_dim)), axis=1)
    cv2.imshow('window', stitch)
    # cv2.imshow('window', frame)
    t_f = time.time()
    raw_capture.truncate(0)

    dur = t_f-t_i
    # print(dur, 'sec')

    if cv2.waitKey(1) == ord('q'):
        send_angle_r(0,0)
        print('detection rate', np.round(found/(found+notfound), 2)*100, '%')
        print('frame rate:', np.round((found+notfound)/dur, 1), 'fps')
        break

camera.release()
cv2.destroyAllWindows()
