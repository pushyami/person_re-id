"""
This is V1 of recording for foscam streams

TODO

python3 cam_name url duration

e.g.

python3 doggie_cam 111111 'http://111.111.111.111/axis-cgi/mjpg/video.cgi' 1

cam_name = arbitrary name you call your video
url = the url to the page that streams the video
duration = in minutes e.g 1 stands for 1 minute

V1 first opens three web pages for streaming to happen and then records it using openCV's built-in function

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

import webbrowser

#from selenium import webdriver

#ip = 'http://128.46.75.113:88'
#cam_name = 'Camera3'
#pwd = 't5SPhjz@fmH'

"""
Read Arguments and store in the variables cam_name, pwd, ip, duration and set url format to read the camera
"""
cam_name = str(sys.argv[1])
pwd = str(sys.argv[2])
ip = str(sys.argv[3])
duration = float(sys.argv[4])

urlsetmain = ip + ':88/cgi-bin/CGIProxy.fcgi?cmd=setMainVideoStreamType&streamType=0&usr=' + cam_name + '&pwd=' + pwd
print (urlsetmain)
urlsetsub = ip + ':88/cgi-bin/CGIProxy.fcgi?cmd=setSubStreamFormat&format=1&usr=' + cam_name + '&pwd=' + pwd
urlmj = ip + ':88/cgi-bin/CGIStream.cgi?cmd=GetMJStream&usr=' + cam_name + '&pwd=' + pwd

#r = requests.get(urlsetmain)
#print (r)
webbrowser.open(urlsetmain)
time.sleep(3)
webbrowser.open(urlsetsub)
time.sleep(3)
webbrowser.open(urlmj)
time.sleep(10)

#r = requests.get(urlsetsub)
#print (r)

#dr = webdriver.Chrome()

cap = cv2.VideoCapture(urlmj)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

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

out = cv2.VideoWriter(file_name,fourcc,20.0,(frame_width,frame_height))


#set the end time, sec = duration * 15 is experimental, should be changed
sec = duration * 15.0

t_start = datetime.datetime.now()
t_end = t_start + datetime.timedelta(minutes = duration, seconds = sec)


#record before t_end
while True:
#while datetime.datetime.now() < t_end:
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


