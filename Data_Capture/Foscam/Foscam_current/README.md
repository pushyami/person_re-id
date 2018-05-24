Directory for scheduling video capture on Foscam devices

Dependencies: 
  - Run in venv using the command 'source venv/bin/activate' from home directory
  - Python imports/other installs needed:
      - opencv
      - requests
      - venv
      - urllib
      - numpy

foscam_scheduler_v1.2.py is for foscam capture ***only***
  - URL stream must be open in local browser for the video capture portion of the program to correctly record the stream

***ip_scheduler.py is current working version***
To do:
- input history
- file redirection
- automate videopath
- search tools (IP, country, state, city, type, etc.)
- dependency installation script
