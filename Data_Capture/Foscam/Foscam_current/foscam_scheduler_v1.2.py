"""
	Version 2
		
	Single-process, multi-thread execution
	MUST be left OPEN in terminal (threads are not daemons)
	
	To launch: python foscam_scheduler_v1.2.py
	Usage: camera_name password ip date time duration
	Ex:
		Enter new capture > Camera1 *********** 128.46.75.*** 052418 1230 0.5
	Schedules the given camera to capture a half-minute long video on May 24th, 2018 at 12:30PM

"""

import threading
from datetime import datetime
from datetime import timedelta
import cv2
import urllib
import numpy as np
import time
import requests
import re
import subprocess as s
import os, sys

def exec_capture(*user_input):

	#Retrieve username, password, and camera ip address from arguments
	user = user_input[0]
	password = user_input[1]
	ip = user_input[2]

	ip = 'http://' + ip

	#Retrieve date to execute capture
	month = user_input[3][0:2]
	day = user_input[3][2:4]
	year = user_input[3][4:]

	#formats year
	#ex: 18 goes to 2018
	if (len(year) != 4):
		year = '20' + year

	#Retrieves time to execute capture (in military time)
	hour = user_input[4][0:2]
	minute = user_input[4][2:]

	#duration of capture in minutes
	duration = user_input[5]

	#cast datetimes to ints
	month = int(month)
	day = int(day)
	year = int(year)
	hour = int(hour)
	minute = int(minute)

	#create datetime object of execution date
	exec_datetime = datetime(year, month, day, hour, minute)

	#creates current datetime object
	curr_datetime = datetime.now()

	#checks for valid execution date (also handled in part by datetime object value bounds)
	if (exec_datetime < curr_datetime):
		print('Date or time has elapsed already')
		sys.exit()
		
	#write 'command made' log to master file as
	"""
	Current date and time
	Capture will be set for:
	month/day/year at hour:minute for duration minutes
	On camera username, password, ip
	Process id: pid
	"""
	exec_file = open('camera_exec_log.out', 'a')
	curr_datetime = datetime.now()
	exec_file.write(str(curr_datetime) + '\n')
	exec_file.write('Capture will be set for: ')
	exec_file.write(str(month) + '/' + str(day) + '/' + str(year) + ' at ' + str(hour) + ':' + str(minute) + ' for ' + str(duration) + ' minutes.\n')
	exec_file.write('On camera ' + user + ', ' + password + ', ' + ip + '\n')
	exec_file.write('Process id: ' + str(os.getpid()) + '\n')
	#separator for easy reading in log file
	exec_file.write('-----------------------------------------------------------------\n')
	exec_file.close()

	#main piece, 'sleeps' the process until execution time
	while (exec_datetime > curr_datetime):
		#updates current datetime
		curr_datetime = datetime.now()

	#writes log to master file as
	"""
	Current date and time
	Executing duration minutes capture on stream ip, username, password
	"""
	exec_file = open('camera_exec_log.out', 'a')
	curr_datetime = datetime.now()

	#Execution message with detail
	exec_message = 'Executing ' + duration + ' minute capture on stream ' + ip + ', ' + user + ', ' + password + '\n'

	#gives desktop notification on execution
	s.call(["notify-send", "-i", "image-loading", exec_message])

	#write log to file
	exec_file.write(str(curr_datetime) + '\n')
	exec_file.write(exec_message)
	exec_file.write('-----------------------------------------------------------------\n')
	exec_file.close()

	#calls the video capture script here
	#-------------------------
	
	cam_name = user
	pwd = password
	ip = ip
	duration = float(duration)

	urlsetmain = ip + ':88/cgi-bin/CGIProxy.fcgi?cmd=setMainVideoStreamType&streamType=0&usr=' + cam_name + '&pwd=' + pwd
	urlsetsub = ip + ':88/cgi-bin/CGIProxy.fcgi?cmd=setSubStreamFormat&format=3&usr=' + cam_name + '&pwd=' + pwd
	urlmj = ip + ':88/cgi-bin/CGIStream.cgi?cmd=GetMJStream&usr=' + cam_name + '&pwd=' + pwd

	r = requests.get(urlsetmain, timeout=10)
	
	r = requests.get(urlsetsub, timeout=10)
	
	cap = cv2.VideoCapture(urlmj)

	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))

	fourcc = cv2.VideoWriter_fourcc(*'XVID')

	date_time = (str(datetime.now())).split()

	date = re.findall('\d+', date_time[0])
	date = (''.join(date))

	time = re.findall('\d+', date_time[1])
	time = (''.join(time))[:6]
	file_name = cam_name + '_' + date + '_' + time + '.avi'

	out = cv2.VideoWriter(file_name,fourcc,20.0,(640,480))

	sec = duration * 15.0

	t_start = datetime.now()
	t_end = t_start + timedelta(minutes = duration, seconds = sec)

	while True:
	#while datetime.datetime.now() < t_end:
		ret, frame = cap.read()
		
		out.write(frame)
		#cv2.imshow('frame',frame)
			 
		if datetime.now() >= t_end:
			break

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	out.release()
	cv2.destroyAllWindows()

	#-------------------------


user_input = 'Usage: camera_name password ip_address date time duration'
print(user_input)

while (True):
	user_input = input("Enter new capture > ").split(' ')
	if (user_input[0] == 'exit'):
		sys.exit()	
	new_thread = threading.Thread(target=exec_capture, args=(user_input))
	new_thread.start()

sys.exit()
