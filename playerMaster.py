"""
Class PlayerThread
- this class is the extension of class Thread
- major task: receiving message from clients, change/update the egg
- to trigger the thread -> playerThread.run() or playerThread.start()
"""
import socket
import threading
import json

class serverMsg:
	REQUESTTYPE = ""
	OBJECTTYPE = ""
	DATA = ""
	XCOORDINATE = ""
	YCOORDINATE = ""

	# constructor
	def __init__(self, requestType, objectType, objectData, xCoorindate, yCoordinate,
		visible, lockState, occupyState, ownerID):
		self.REQUESTTYPE = requestType
		self.OBJECTTYPE = objectType
		self.XCOORDINATE = xCoorindate
		self.YCOORDINATE = yCoordinate
		self.VISIBLE = visible
		self.LOCKSTATE = lockState
		self.OCCUPYSTATE = occupyState
		self.OWNERID = ownerID


# playerThread - child of class Threading 
class playerAdmin(threading.Thread):
	# playerThread configuration
	CLIENTSOCKET = None
	PLAYER_THREAD = None
	BUF_SIZE = 1024
	MUTEX = None
	LAST_MSG = ""		# QUEUE_MSG - collect & store user's request - keep the last request

	# Gameplay properties
	EGGHOLDING = None 	# EGGHOLDING - keep the egg object that players is currently working on
	DICT_EGG = None 	# DICT_EGG - reference of DICT_EGG from server

	# Constructor
	def __init__(self, clientAddress, threadName, clientSocket, clientSocketThread, bufferSize, dictEggObj, mutex):
		threading.Thread.__init__(self)
		self.threadID = clientAddress			# use clientAddress as threadID
		self.name = threadName
		self.CLIENTSOCKET = clientSocket
		self.PLAYER_THREAD = clientSocketThread 
		self.BUF_SIZE = bufferSize
		self.DICT_EGG = dictEggObj
		self.MUTEX = mutex

	# run() - override run() -> trigger the thread to start
	def run(self):
		# while the game is running -> listen to any update
		while True:
			#listen to any message from client	
			rawData = self.CLIENTSOCKET.recv(self.BUF_SIZE)
			msgData = rawData.decode("utf_8")

			# not valid data - receive 0 bytes
			if not msgData:
				#disconnect
				print("{} disconnect from server".format(self.threadID))
				#need to clean everything after the player get disconnected
				#write the code here
				break

			# valid request:
			else:
				# Store the message -> allow to process the next one
				self.LAST_MSG = msgData
				print("{}: {}".format(self.threadID, self.LAST_MSG))
				
				# Acquire mutex to process:
				self.MUTEX.acquire(1)

				# Try to do handle request - playerAdmin only take care of LOCK & OCCUPY request:

				# access LAST_MSG -> decode LAST_MSG

				# "LOCK":

				# "OCCUPY":

				# Relaese the key for the next user
				self.MUTEX.release()

		return None

	# lockEgg() - clients requests to lock an egg
	# Client acquire key -> to update the egg.lockState & egg.ownerID
	# Successfully lock -> True; otherwise -> False
	def lockEgg(self, eggCoordinate):
		# trigger notification flag
		lockSuccess = False

		# Access the egg 
		egg = self.DICT_EGG[eggCoordinate]

		# Use "try" and "finally" to guarantee action
		# If egg is not being locked/occupied by anyone 
		# -> allow to lock the egg -> trigger notification of success/failure
		if egg != None and egg.isLock() == False and egg.isOccupied == False:
			# Switch lockState to True:
			egg.setLock(True)
			egg.setEggOwnerID = self.threadID

			# hold the egg in EGGHOLDING - Prevent deadlock:
			self.EGGHOLDING = egg
			lockSuccess = True
	
		return lockSuccess


	# occupyEgg() - clients request to occupy an egg
	# Client acquire key -> to update the egg.occupyState & egg.ownerID
	# Successfully occupy -> True; otherwise -> False
	def occupyEgg(self, eggCoordinate):
		#trigger notification flag
		occupySuccess = False

		# Access the egg
		egg = self.DICT_EGG[eggCoordinate]

		# If egg is being locked by the same person who occupy
		# -> allow to occupy the egg -> trigger notification of success/failure
		if egg != None and egg.isLock() == True and egg.getOwnerID() == self.threadID:
			#Switch occupyState to True & visibleState to False:
			egg.setOccupy(True)
			egg.setVisible(False)

			#release EGGHOLDING -> for the next egg:
			self.EGGHOLDING = None
			occupySuccess = True

		return occupySuccess

	# rmvDisconnectPlayer - free the thread for next user (reuse)
	def rmvDisconnectPlayer(self):
		pass

	# sendMsgToPlayer() - send message back to clients
	def sendMsgToPlayer(self, msgContent):
		self.CLIENTSOCKET.send(bytes(msgContent,"utf-8"))
		return None

	# sendMsgToOtherPlayer() - send message to other player
	def sendMsgToOtherPlayer(self, msgContent):
		for key in self.PLAYER_THREAD:
			if key != self.CLIENTSOCKET:
				self.PLAYER_THREAD[key].CLIENTSOCKET.send(bytes(msgContent,"utf-8"))
		return None


    #----------------------------------------------------
    # MESSAGE ENCODE/DECODE
    #----------------------------------------------------

	# decodePlayerMsg() - decode the player mssage to Dictionary
	def decodeMsgToObject(self, userMsg):
		return json.loads(userMsg)

	# prepMsgAsJson()
	def prepMsgAsJson(self, requestType, objectType , anyObject):
		finalMsg = serverMsg(requestType, objectType, self.convertToJson(anyObject))
		return finalMsg

	# convertMsgToJson() - convert egg object to json format
	def convertMsgToJson(self, anyObject):
		return json.dumps(anyObject.__dict__)