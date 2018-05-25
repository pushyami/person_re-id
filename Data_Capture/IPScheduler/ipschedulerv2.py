"""
	Version 2.0
	IP-camera version of foscam_integrated
		
	To launch: python ip_scheduler.py
	Usage: camera_name ip/video_path date time duration
	
	Ex:

		python ip_scheduler.py
		Enter new capture > doggie http://173.165.152.131/axis-cgi/mjpg/video.cgi 052418 1630 1 
	
	Captures a 1 minute video on the given feed on May 24th, 2018 at 4:30PM

	TO BE FIXED:
		- Implement videopath_retriever separately then integrate
		- For now, full video path and IP are both needed	
		- Next version will be able to take only IP and automatically 
		  retrieve the matching videopath

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
	videopath = user_input[1]

	#Retrieve date to execute capture
	month = user_input[2][0:2]
	day = user_input[2][2:4]
	year = user_input[2][4:]

	#formats year
	#ex: 18 goes to 2018
	if (len(year) != 4):
		year = '20' + year

	#Retrieves time to execute capture (in military time)
	hour = user_input[3][0:2]
	minute = user_input[3][2:]

	#duration of capture in minutes
	duration = user_input[4]

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
	exec_file.write('On camera ' + user + ', ' + videopath + '\n')
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
	exec_message = 'Executing ' + duration + ' minute capture on stream ' + videopath + ', ' + user + '\n'

	#gives desktop notification on execution
	s.call(["notify-send", "-i", "image-loading", exec_message])

	#write log to file
	exec_file.write(str(curr_datetime) + '\n')
	exec_file.write(exec_message)
	exec_file.write('-----------------------------------------------------------------\n')
	exec_file.close()

	#Will be getting video path given the ip (implement first in videopath_retriever.py)
	#-------------------------
	
	#	do something here

	#------------------------
	

	#calls the video capture script here
	#-------------------------
	
		
		#this works, but trying to integrate both files together
		#os.system('python bennie.py ' + user + ' ' + videopath + ' ' + duration)
		#-------------------------

	
	cam_name = user
	ip = videopath
	duration = float(duration)
	
	urlmj = ip

	cap = cv2.VideoCapture(urlmj)

	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))

	#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
	fourcc = cv2.VideoWriter_fourcc(*'XVID')

	#-------------------Setting the name of the output video file--------------------"

	date_time = (str(datetime.now())).split()

	date = re.findall('\d+', date_time[0])
	date = (''.join(date))

	time = re.findall('\d+', date_time[1])
	time = (''.join(time))[:6]
	file_name = cam_name + '_' + date + '_' + time + '.avi'

	#-------------------Setting the name of the output video file--------------------"

	out = cv2.VideoWriter(file_name,fourcc,6.4,(int(cap.get(3)),int(cap.get(4))))
	
	#set the end time, sec = duration * 15 is experimental, should be changed
	sec = duration * 15.0

	t_start = datetime.now()
	t_end = t_start + timedelta(minutes = duration, seconds = sec)
	#t_end = t_start + datetime.timedelta(minutes = duration)

	#record before t_end
	while True:
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

#initial message
user_input = 'Usage: camera_name ip_address/video_path date time duration'
print(user_input)
print("Enter 'exit' to close")

#take input until user inputs "exit"
while (True):
	#get input and split into arguments
	user_input = input("Enter new capture > ").split(' ')
	
	#exit on command
	if (user_input[0] == 'exit'):
		sys.exit()	
	
	#spawn and start new standby thread
	#executes wait and video capture
	new_thread = threading.Thread(target=exec_capture, args=(user_input))
	new_thread.start()

sys.exit()
