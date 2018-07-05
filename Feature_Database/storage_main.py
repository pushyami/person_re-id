import threading
import re_id
import queue

def start_queue(Lock):
	timeout = queue.Queue(maxsize=0)
		

def main():
	lock = threading.Lock()
	queue_thread = threading.Thread(target=start_queue, args=(lock,))	
	queue_thread.start()
	queue_thread.join()
	
	

if __name__ == "__main__":
	main()	
