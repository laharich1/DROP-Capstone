import cv2
import numpy as np
# import the necessary packages
import time # Provides time-related functions

# Initialize the camera
camera = cv2.VideoCapture(0)

frame_width = int(camera.get(3))
frame_height = int(camera.get(4))

size = (frame_width, frame_height)

t_i = time.time()
video = cv2.VideoWriter(str(t_i)+'.mp4',
						cv2.VideoWriter_fourcc(*'MP4V'),
						30, size)
while(True):

    ret, frame = camera.read()
    d_t = time.time() - t_i

    video.write(frame)
    # cv2.imshow('Frame',frame)


    if cv2.waitKey(1) == ord('q') or d_t > 20:
        break

camera.release()
cv2.destroyAllWindows()
