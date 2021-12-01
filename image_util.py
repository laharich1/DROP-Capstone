import numpy as np

def distance(n1, n2):
    return  np.sqrt(np.square(np.sum(n1 - n2)))


def chooseCircle(circles, prev_loc, img_center):
    if prev_loc == None:
        prev_loc = img_center

    centers = circles[0, :, :2]
    dist = distance(centers, prev_loc)
    arg_target = np.argmin(dist)

    target_center = (circles[0, arg_target, 0], circles[0, arg_target, 1])
    target_radius = circles[0, arg_target, 2]
    return target_center, target_radius


def relativeLocation(target_center, img_center):
    disp = (img_center[0]-target_center[0], img_center[1]-target_center[1])
    dist = np.sqrt(disp[0]**2 + disp[1]**2)
    angle = (np.arctan2(disp[0], disp[1]) + np.pi/2) % (2*np.pi)
    maxDist = np.sqrt(img_center[0]**2 + img_center[1]**2)

    return (dist/maxDist), angle
