#UNCOMMENTED VERSION OF FOSCAM_RECORD.PY

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

print (sys.argv[1])


#ip = 'http://128.46.75.113:88'
#cam_name = 'Camera3'
#pwd = 't5SPhjz@fmH'

cam_name = str(sys.argv[1])
pwd = str(sys.argv[2])
ip = str(sys.argv[3])
duration = float(sys.argv[4])

urlsetmain = ip + ':88/cgi-bin/CGIProxy.fcgi?cmd=setMainVideoStreamType&streamType=0&usr=' + cam_name + '&pwd=' + pwd
print (urlsetmain)
urlsetsub = ip + ':88/cgi-bin/CGIProxy.fcgi?cmd=setSubStreamFormat&format=3&usr=' + cam_name + '&pwd=' + pwd
urlmj = ip + ':88/cgi-bin/CGIStream.cgi?cmd=GetMJStream&usr=' + cam_name + '&pwd=' + pwd

r = requests.get(urlsetmain, timeout=10)
print (r)

r = requests.get(urlsetsub, timeout=10)
print (r)

cap = cv2.VideoCapture(urlmj)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

fourcc = cv2.VideoWriter_fourcc(*'XVID')

print (datetime.datetime.now())

date_time = (str(datetime.datetime.now())).split()

date = re.findall('\d+', date_time[0])
date = (''.join(date))

time = re.findall('\d+', date_time[1])
time = (''.join(time))[:6]
file_name = cam_name + '_' + date + '_' + time + '.avi'

print (file_name)

out = cv2.VideoWriter(file_name,fourcc,20.0,(640,480))

sec = duration * 15.0

t_start = datetime.datetime.now()
t_end = t_start + datetime.timedelta(minutes = duration, seconds = sec)

while True:
#while datetime.datetime.now() < t_end:
	ret, frame = cap.read()
	
	out.write(frame)
	#cv2.imshow('frame',frame)
 
	if datetime.datetime.now() >= t_end:
		break

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
out.release()
cv2.destroyAllWindows()


