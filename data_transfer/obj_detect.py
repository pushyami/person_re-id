import socket
import cv2
import numpy
import sys

if (len(sys.argv) != 3):
    print("Usage: host_ip host_port")
    exit()

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostbyname(TCP_IP), TCP_PORT))
print("Connection with host made")

capture = cv2.VideoCapture(0)
print("Capturing")

while True:
    ret, frame = capture.read()

    (rects, weights) = hog.detectMultiScale(frame, winStride=(8, 8), padding=(64, 64), scale=1.1)

    if not (rects):
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()

        sock.send( str(len(stringData)).ljust(16));
        sock.send( stringData );

sock.close()
cv2.destroyAllWindows() 
