
"""
This is V1 of recording for the streams of cam2 DB

TODO

python3 cam_name url duration

e.g.

python3 doggie_cam 'http://111.111.111.111/axis-cgi/mjpg/video.cgi' 1

cam_name = arbitrary name you call your video
url = the url to the page that streams the video
duration = in minutes e.g 1 stands for 1 minute

"""

import datetime

import cv2
import urllib
import numpy as np
import os

import time

import urllib
import requests

import re

import sys

"""
Read Arguments and store in the variables cam_name, ip, duration
"""
cam_name = str(sys.argv[1])
ip = str(sys.argv[2])
duration = float(sys.argv[3])

urlmj = ip

cap = cv2.VideoCapture(urlmj)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

#-------------------Setting the name of the output video file--------------------"

date_time = (str(datetime.datetime.now())).split()

date = re.findall('\d+', date_time[0])
date = (''.join(date))

time = re.findall('\d+', date_time[1])
time = (''.join(time))[:6]
file_name = cam_name + '_' + date + '_' + time + '.avi'

print (file_name)

#-------------------Setting the name of the output video file--------------------"

out = cv2.VideoWriter(file_name,fourcc,6.4,(int(cap.get(3)),int(cap.get(4))))


#set the end time, sec = duration * 15 is experimental, should be changed
sec = duration * 15.0

t_start = datetime.datetime.now()
t_end = t_start + datetime.timedelta(minutes = duration, seconds = sec)
#t_end = t_start + datetime.timedelta(minutes = duration)

#record before t_end
while True:
	ret, frame = cap.read()

	out.write(frame)
	cv2.imshow('frame',frame)
	
	if datetime.datetime.now() >= t_end:
		break

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
out.release()
cv2.destroyAllWindows()


