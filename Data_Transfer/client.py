import socket
import cv2
import numpy
import sys
import time

if (len(sys.argv) != 3):
    print("Usage: host_ip host_port")
    exit()

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostbyname(TCP_IP), TCP_PORT))
print("Connection with host made")

capture = cv2.VideoCapture(0)
print("Capturing")

count = 0
curr_count = 0
FPS_rate = 0

start_time = time.time()
while True:
    ret, frame = capture.read()

    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    sock.send( str(len(stringData)).ljust(16));
    sock.send( stringData );
    
    count += 1
    elapsed_time = time.time()
    if (elapsed_time - start_time > 1):
            start_time = time.time()
            FPS_rate = count - curr_count
            curr_count = count
    
    sys.stdout.write("\rFPS:" + str(FPS_rate))

sock.close()
cv2.destroyAllWindows() 
