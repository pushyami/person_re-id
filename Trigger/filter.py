import numpy as np
import cv2
import imutils

min_area = 500

def filter(frame, fgbg):
    flag = False
    
    resize_frame = imutils.resize(frame, width=500)

    fgmask = fgbg.apply(resize_frame)

    im2, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in contours:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_area:
            continue
        else:
            return True

    return False
