import threading
import time

class Timer(threading.Thread):
	def __init__(self, num, interval)
		threading.Thread.__init__(self)
		self.thread_num = num
		self.interval = interval
		self.thread_stop = False

	def run(self):
		while not self.thread_stop:
			
