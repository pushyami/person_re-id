"""
	VERSION 1

	URL STREAM MUST BE OPEN IN BROWSER FOR STREAM TO CAPTURE

	TO BE FIXED:
		- Switch to single process, multiple thread execution
		- Find way to keep process execution running even if the machine is turned off"
"""

import subprocess as s

from datetime import datetime

import os, sys

#also read this as doc
help_message = """
Scheduler for video capture
Process will run in background and will continue exection even if terminal is closed given that the machine is NOT turned off

Usage: python scheduler.py username password ip_address date time duration & disown

Command details:	
	- For camera credentials use the same ones as are used for URL-commands
	- Date should be a 6 or 8 digit number, ex: May 21st, 2018 should be 05212018 (or 052118, it will format 2 digit year to 4 digit anyways)
	- Time is in military time and should be 4 digits, ex: 1:30PM should be 1330
	- Duration is in minutes
	- '& disown' MUST BE IN THE COMMAND to push the process to the background and disassociate from the current terminal
		> This is only for multiple process, single thread execution

Logging:
	- Writes to file 'camera_exec_log.out'
	- Gives date and time of log
	- Logs when execution datetime command is made
	- Logs when execution is actually made (video starts capturing)
"""
	
#help command prints on empty, -h or incorrect number of arguments
if (len(sys.argv) == 1) or (len(sys.argv) != 7) or (sys.argv[1] == '-h'):
	print(help_message)
	sys.exit(0)

#Retrieve username, password, and camera ip address from arguments
user = sys.argv[1]
password = sys.argv[2]
ip = sys.argv[3]

ip = 'http://' + ip

#Retrieve date to execute capture
month = sys.argv[4][0:2]
day = sys.argv[4][2:4]
year = sys.argv[4][4:]

#formats year
#ex: 18 goes to 2018
if (len(year) != 4):
	year = '20' + year

#Retrieves time to execute capture (in military time)
hour = sys.argv[5][0:2]
minute = sys.argv[5][2:]

#duration of capture in minutes
duration = sys.argv[6]

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

#logs to console
print('Capture will be set for: ' + str(month) + '/' + str(day) + '/' + str(year) + ' at ' + str(hour) + ':' + str(minute) + ' for ' + str(duration) + ' minutes.')

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
os.system('python foscam_vid_capture_v1.py ' + user + ' ' + password + ' ' +  ip + ' ' + duration + ' & disown')
#-------------------------

sys.exit()
