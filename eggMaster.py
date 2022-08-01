"""
Class PlayerThread
- this class is the extension of class Thread
- major task: generate new egg position -> add into the dictionary of egg
- to trigger the thread -> eggAdmin.run(gameIsLive, dictEggObj)
"""
import threading
import egg
import time
import random
import json

class eggAdmin(threading.Thread):
	EGG_SEM = None
	EGG_COORDS = None
	EGG_COUNT = 0
	MAX_EGG = 0

	def __init__(self, threadID, threadName, eggSem, eggCoords, maxEggs):
		threading.Thread.__init__(self)
		self.THREADID = threadID
		self.THREADNAME = threadName
		self.EGG_SEM = eggSem
		self.EGG_COORDS = eggCoords
		self.MAX_EGG = maxEggs

	# run() - override run() -> trigger the thread to start
	def run(self):
		while True:
			if self.EGG_COUNT < sef.MAX_EGG:
				# acquire semaphore
				self.EGG_SEM.acquire()

				# generate position for new egg:
				pos = self.generate_egg_position()

				# add new egg to list of eggs
				self.EGG_COORDS.append(pos)
				self.EGG_COUNT += 1

				# release semaphore
				self.EGG_SEM.release()
			else:
				print("max eggs reach")

			# sleep for randome amount of time - avoid create too many eggs
			time.sleep(random.randint(0,4))
		return None


	# generateEggPosition() - randomly generate the position for the new egg
	def generateEggPosition(self):
		pos = (-1,-1)
		while pos == (-1,-1) or pos in self.EGG_COORDS:    
			pos = (random.randint(0, 7)*100, random.randint(0,7)*100)
		return pos
