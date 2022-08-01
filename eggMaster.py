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

class eggMsg:
	REQUESTTYPE = ""
	OBJECTTYPE = ""
	DATA = ""

	# constructor
	def __init__(self, requestType, objectType, objectData):
		self.REQUESTTYPE = requestType
		self.OBJECTTYPE = objectType
		self.DATA = objectData

class eggAdmin(threading.Thread):
	PLAYER_THREAD = None
	DICT_EGG = None
	FINAL_EGG = None
	MAX_EGG = 0
	GAME_LIVE = None

	def __init__(self, threadID, threadName, playerThread, dictEggObj, finalEggObj, maxNumEggs, gameLive):
		threading.Thread.__init__(self)
		self.THREADID = threadID
		self.THREADNAME = threadName
		self.PLAYER_THREAD = playerThread
		self.DICT_EGG = dictEggObj
		self.FINAL_EGG = finalEggObj 
		self.MAX_EGG = maxNumEggs
		self.GAME_LIVE = gameLive

	# run() - override run() -> trigger the thread to start
	def run(self):
		while self.GAME_LIVE[0] == True:
			time.sleep(random.randint(0,4))
			#clear the not VISIBLE eggs:
			#self.cleanHatchingEgg()


			# generate new egg at random rate
			if (1 - len(self.DICT_EGG)/self.MAX_EGG) > 0.4:
				newEggPos = self.generateEggPosition()

				# Add new Egg into DICT_EGGS_OBJ
				# EggNode(xCoordinate, yCoordinate, visible, lock, occupy, points)
				newEgg = egg.EggNode(newEggPos[0], newEggPos[1], True, True, True, 1)
				self.DICT_EGG[newEggPos] = newEggPos 
				
				# Send the egg object to client
				sendEggMsg = self.prepMsgAsJson("add", "egg", newEgg)
				print(self.convertToJson(sendEggMsg))
				self.sendEggToClient(self.convertToJson(sendEggMsg))
		return None

	# sendEggToClient() - send egg to clients
	def sendEggToClient(self, eggCoordinate):
		for key in self.PLAYER_THREAD:
			self.PLAYER_THREAD[key].CLIENTSOCKET.send(bytes(eggCoordinate,"utf-8"))
		return None	

	# generateEggPosition() - randomly generate the position for the new egg
	def generateEggPosition(self):
		pos = (-1,-1)
		while pos == (-1,-1) or pos in self.DICT_EGG:    
			pos = (random.randint(0, 7)*100, random.randint(0,7)*100)
		return pos

	# cleanHatchingEgg() - remove all hatching eggs out of DICT_EGG
	def cleanHatchingEgg(self):
		for key in self.DICT_EGG:
			# if egg no longer visible to draw -> move to FINAL_EGG:
			if self.DICT_EGG[key].isVisible() == False:

				# pop the egg out of DICT_EGG
				egg = self.DICT_EGG.pop(key)

				# append egg to FINAL_EGG list
				self.FINAL_EGG.append(egg)
		return None

	# prepMsgAsJson()
	def prepMsgAsJson(self, requestType, objectType, anyObject):
		finalMsg = eggMsg(requestType, objectType, self.convertToJson(anyObject))
		return finalMsg

	# convertEggToJson() - convert egg object to json format
	def convertToJson(self, anyObject):
		return json.dumps(anyObject.__dict__)