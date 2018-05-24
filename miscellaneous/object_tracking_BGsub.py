"""Simple object tracking algorithm that tracks objects using background subtraction
   and then identifies similar contours. Written with the help of the opencv library"""

import cv2 as cv2
import numpy as np
import sys

#Checking for the right inputs to the program:
if(len(sys.argv) < 2):
    print("Usage: object_trackingBGsub.py <videoname>")
    quit()

#Creating the video object
cap = cv2.VideoCapture(sys.argv[1])

#Creating the BG Subtractor:
fgbg = cv2.createBackgroundSubtractorMOG2()

#Creating a list of all bboxes present:
bboxes_present = []

#Creaating a delta of values within which no motion is detected:
DELTA = 1000

#Reading in the video itself:
while(cap.isOpened()):
    #Read the next frame
    ret,frame = cap.read()

    #Apply BG subtraction:
    fgmask = fgbg.apply(frame)

    #Get the related contours:
    im2, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Obtaining all bboxes from the contours:
    for i in range(len(contours)):
        if(cv2.contourArea(contours[i]) > 1500):
            x,y,w,h = cv2.boundingRect(contours[i])

            #check whether this bounding box already present:
            flag = False
            for j in range(DELTA):
                if((x+i,y+i,w+i,h+i) in bboxes_present):
                    flag = True
                elif((x-i,y-i,w-i,h-i) in bboxes_present):
                    flag = True

            #If the value is not within delta, then it means that the object is in motion:
            if(not flag):
                cv2.rectangle(frame,(x,y),(x+w,y+h), (0,0,255), 2)
        
    # Display resulting frame
    cv2.imshow("Tracking", frame)
 
    # Exit if ESC pressed
    k = cv2.waitKey(25) & 0xff
    if k == 27 : break