import socket
import cv2
import numpy
import sys
import os
import time
import logging
import threading

caffe_root = '~/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe

if ((len(sys.argv) != 2) and ((len(sys.argv) == 3) and (sys.argv[2] != "-s"))):
	print("Usage: port [ -s ]")
	exit()

model = "./hw2-deploy.prototxt"
weights = "./hw2-weights.caffemodel"

caffe.set_device(0)
caffe.set_mode_gpu()

net = caffe.Net(model, weights, caffe.TEST)
print("Model loaded")

nnInputWidth = 32
nnInputHeight = 32
total = 0
num = 0

cam_counter = 0
#
#
#	 NON-SYSTEMS PEOPLE DO YOUR STUFF HERE
#	 
#
#=====================================
def _POLO_(frame_name, frame):
	image = frame
	global total
	global num
	inputResImg = cv2.resize(image, (nnInputWidth, nnInputHeight), interpolation=cv2.INTER_CUBIC)
	transposedInputImg =inputResImg.transpose(2,0,1)
	net.blobs['data'].data[...]=transposedInputImg
	out = net.forward()
	max_value=0
	max_iter=-1
	total = total + 1
	for y in out:
		scores = out[y]
		for x in range(len(scores[0])):
			k = scores[0][x]
			if k > max_value:
				max_value = k
				max_iter = x
	
				#if max_iter== int(l[1]):
#					print "YES"
				#	num = num +1
#		print scores, max_iter
		print scores
#	print "\n"

	logging.info("Accuracy: ", num*1.0/total)
		
#=====================================

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_PORT = int(sys.argv[1])
CAM_NAME = "cam" + str(cam_counter)

def Main():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostbyname("128.46.75.212"), TCP_PORT))
        s.listen(True)
        logging.info("Server launched")

        while True:
                conn, addr = s.accept()
                logging.info("Connection established on port " + str(TCP_PORT))
                start_new_thread(threaded_func, (conn,))
                cam_counter += 1

        logging.info("Connection closed")
        s.close()
        cv2.destroyAllWindows() 

def threaded_func(conn):
    CAM_NAME = "cam" + str(cam_counter)
    
    if(not os.path.exists("./cam" + str(cam_counter))):
            os.makedirs("cam" + str(cam_counter))

    count = 0
    curr_count = 0
    FPS_rate = 0
                                   
    start_time = time.time()
    while True:
	length = recvall(conn,16)
	if length is None:
		break;
	stringData = recvall(conn, int(length))
	data = numpy.fromstring(stringData, dtype='uint8')

	decimg = cv2.imdecode(data, 1)
	_POLO_(CAM_NAME, decimg)	

	if (len(sys.argv) == 3 and sys.argv[2] == "-s"):	
		cv2.imshow(CAM_NAME, decimg)
		if (cv2.waitKey(1) & 0xFF == ord('q')):
			break;
	elif (len(sys.argv) == 2):
		cv2.imwrite(CAM_NAME + "/" + CAM_NAME + "_" + str(count % 9001) + ".jpg", decimg)
	
	count += 1
	elapsed_time = time.time()
	if (elapsed_time - start_time > 1):
		start_time = time.time()
		FPS_rate = count - curr_count
		curr_count = count

	sys.stdout.write("\rPacket size:" + str(int(length)) + " | FPS:" + str(FPS_rate))

if __name__ == "__main__":
        Main()
