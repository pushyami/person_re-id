"""
This version first finds the average fps of a one minute stream and then reads the frames.
It writes the frames into the an avi/mp4 file

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

from collections import Counter

cam_name = str(sys.argv[1])
ip = str(sys.argv[2])
duration = float(sys.argv[3])

urlmj = ip

#-------------------Setting the name of the output video file--------------------"

date_time = (str(datetime.datetime.now())).split()

date = re.findall('\d+', date_time[0])
date = (''.join(date))

time = re.findall('\d+', date_time[1])
time = (''.join(time))[:6]
file_name = cam_name + '_' + date + '_' + time + '.avi'

print (file_name)

#-------------------Setting the name of the output video file--------------------"

urlmj = ip

cap = cv2.VideoCapture(urlmj)

#cap = cv2.VideoCapture('stopwatch.mp4')

start = datetime.datetime.now()

t_start = datetime.datetime.now()
t_end = t_start + datetime.timedelta(minutes = 1.0)

h_start = start

#out = cv2.VideoWriter(file_name,fourcc,20.0,(int(cap.get(3)),int(cap.get(4))))

i = 0
j = 0

fps = []
total_fps = 0.0
count = 0.0

while True:
	#print ('')
	#print (datetime.datetime.now())

#for i in range(1000):
	
	i += 1.0
	j += 1.0

	ret,frame = cap.read()

	if ret == False:
		break

	#cv2.imshow('frame',frame)

	if datetime.datetime.now() >= t_end:
		break

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	end = datetime.datetime.now()
	difference = (end - h_start).total_seconds()

	if difference >= 1.0:
		h_start = datetime.datetime.now()
		fps.append(j)
		total_fps += (j/difference)
		count += 1.0
		j = 0

end = datetime.datetime.now()

difference = (end - start).total_seconds()

print (start,'|',end,'|',difference)
print (fps,total_fps,(total_fps/count))
print (i,(i/difference))

print (Counter(fps), Counter(fps).most_common()[0])

set_fps = Counter(fps).most_common()[0]

print (set_fps[0],set_fps)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

change_fps = set_fps[0]

out = cv2.VideoWriter(file_name,fourcc,change_fps,(int(cap.get(3)),int(cap.get(4))))

t_start = datetime.datetime.now()
t_end = t_start + datetime.timedelta(minutes = duration)

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