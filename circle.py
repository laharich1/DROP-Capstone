import cv2
import numpy as np
from image_util import *

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
prev_loc = None

while(True):

    ret, frame = capture.read()

    if not (capture.isOpened()):
        print("device not found")

    rows = frame.shape[0]
    cols = frame.shape[1]
    img_center = (cols//2, rows//2)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    ret, thr = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(thr, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                param1=100, param2=35,
                                minRadius=1, maxRadius=100)

    thr2 = np.zeros_like(frame)
    thr2[:,:,0] = thr
    thr2[:,:,1] = thr
    thr2[:,:,2] = thr

    if circles is not None:
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

    if target_center != None:
        top_left = (target_center[0]-target_radius, target_center[1]-target_radius)
        bot_right = (target_center[0]+target_radius, target_center[1]+target_radius)
        cv2.rectangle(frame, top_left, bot_right, (255, 0, 0), 3)

        start = img_center
        end = target_center
        cv2.line(frame, start, end, (0,255,0), 2)
        dist, angleR = relativeLocation(target_center, img_center)
        print('angle:', np.around(np.degrees(angleR),2))


    # thr = np.flip(thr, axis=1)
    # frame = np.flip(frame, axis=1)
    #
    # cv2.imshow('window', thr)
    # cv2.imshow('window2', frame)

    r_dim = (cols//2, rows//2)
    stitch = np.concatenate((cv2.resize(frame,r_dim), cv2.resize(thr2,r_dim)), axis=1)
    cv2.imshow('window', stitch)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
