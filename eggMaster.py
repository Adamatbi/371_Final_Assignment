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

class eggAdmin(threading.Thread):
	def __init__(self, threadID, threadName, setToDaemon, dictEggObj):
		threading.Thread.__init__(self)
		self.THREADID = threadID
		self.THREADNAME = threadName
		self.ISDAEMON = setToDaemon
		self.DICT_EGG = dictEggObj 

	# run() - override run() -> trigger the thread to start
	def run(self, gameIsLive, maxNumEggs):
		# while the game still running:
		while gameIsLive:

			#if number of current eggs < than max number of eggs -> generate
			if len(self.DICT_EGG) < maxNumEggs:

				#sleep for random amount of time between 1 - 4 seconds
				time.sleep(random.randint(0,4))

				# generate new egg
				newEggPos = self.generateEggPosition()

				# Add new Egg into DICT_EGGS_OBJ
				# EggNode(xCoordinate, yCoordinate, visible, lock, occupy, points)
				newEggPos = egg.EggNode(newEggPos[0], newEggPos[1], True, True, True, 1)
				self.DICT_EGG[newEggPos] = newEggPos 
				
				# Send the egg object to client
				print(newEggPos.getCoordinate())
		return None


	# generateEggPosition() - randomly generate the position for the new egg
	def generateEggPosition(self):
		pos = (-1,-1)
		while pos == (-1,-1) or pos in self.DICT_EGG:    
			pos = (random.randint(0, 7)*100, random.randint(0,7)*100)
		return pos