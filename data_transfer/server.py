import socket
import cv2
import numpy
import sys
import os

if ((len(sys.argv) != 3) and ((len(sys.argv) == 4) and (sys.argv[3] != "-s"))):
	print("Usage: port camera_name [ -s ]")
	exit()

if not os.path.exists("./" + sys.argv[2]):
	os.makedirs(sys.argv[2])

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_PORT = int(sys.argv[1])
CAM_NAME = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname("128.46.75.212"), TCP_PORT))
s.listen(True)
print("Server launched")

conn, addr = s.accept()
print("Connection established on port " + str(TCP_PORT))

count = 0

while True:
	length = recvall(conn,16)
	sys.stdout.write("\rPacket size:" + str(length))
	stringData = recvall(conn, int(length))
	data = numpy.fromstring(stringData, dtype='uint8')

	decimg = cv2.imdecode(data, 1)
	
	count += 1

	if (len(sys.argv) == 4 and sys.argv[3] == "-s"):	
		cv2.imshow(CAM_NAME, decimg)
		if (cv2.waitKey(1) & 0xFF == ord('q')):
			break;
	elif (len(sys.argv) == 3):
		cv2.imwrite(CAM_NAME + "/" + CAM_NAME + "_" + str(count % 9001) + ".jpg", decimg)
	
s.close()
cv2.destroyAllWindows() 
