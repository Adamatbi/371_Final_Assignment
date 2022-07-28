"""
Class PlayerThread
- this class is the extension of class Thread
- major task: receiving message from clients, change/update the egg
- to trigger the thread -> playerThread.run() or playerThread.start()
"""
import socket
import threading

# playerThread - child of class Threading 
class playerThread(threading.Thread):
	# playerThread configuration
	CLIENTSOCKET = None
	CLIENTADDRESS = None
	BUF_SIZE = 1024
	MUTEX = None

	# Gameplay properties
	EGGHOLDING = None 	# EGGHOLDING - keep the egg object that players is currently working on
	DICT_EGG = None 	# DICT_EGG - reference of DICT_EGG from server

	# Constructor
	def __init__(self, threadID, threadName, clientSocket, clientAddress, bufferSize, dictEggObj, mutex):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = threadName
		self.CLIENTSOCKET = clientSocket
		self.CLIENTADDRESS = clientAddress 
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
				#print("{}: {}".format(self.threadID, msgData))
				#react based on the client's request
				#write the code here
		return None

	# lockEgg() - clients requests to lock an egg
	# Client acquire key -> to update the egg.lockState & egg.ownerID
	# Successfully lock -> True; otherwise -> False
	def lockEgg(self, eggCoordinate):
		# trigger notification flag
		lockSuccess = False

		# Obtain the key - to access DICT_EGG - timeout to 1 second -> prevent deadlock
		self.MUTEX.acquire(1)
		
		# Access the egg 
		egg = self.DICT_EGG[eggCoordinate]

		# Use "try" and "finally" to guarantee action
		# If egg is not being locked/occupied by anyone 
		# -> allow to lock the egg -> trigger notification of success/failure
		try:
			if egg.isLock() == False and egg.isOccupied == False:
				# Switch lockState to True:
				egg.setLock(True)
				egg.setEggOwnerID = self.threadID

				# hold the egg in EGGHOLDING - Prevent deadlock:
				self.EGGHOLDING = egg
				lockSuccess = True
			
		# Release the key for next user:
		finally:
			self.MUTEX.release()

		return lockSuccess


	# occupyEgg() - clients request to occupy an egg
	# Client acquire key -> to update the egg.occupyState & egg.ownerID
	# Successfully occupy -> True; otherwise -> False
	def occupyEgg(self, eggCoordinate):
		#trigger notification flag
		occupySuccess = False

		# Obtain the key - to access DICT_EGG - timeout to 1 second -> prevent deadlock
		self.MUTEX.acquire(1)

		# Access the egg
		egg = self.DICT_EGG[eggCoordinate]

		# If egg is being locked by the same person who occupy
		# -> allow to occupy the egg -> trigger notification of success/failure
		try:
			if egg.isLock() == True and egg.getOwnerID() == self.threadID:
				#Switch occupyState to True & visibleState to False:
				egg.setOccupy(True)
				egg.setVisible(False)

				#release EGGHOLDING -> for the next egg:
				self.EGGHOLDING = None
				occupySuccess = True

		# Relaese the key for the next user
		finally:
			self.MUTEX.release()

		return occupySuccess

	# rmvDisconnectPlayer - free the thread for next user (reuse)
	def rmvDisconnectPlayer(self):
		pass

	# sendMsgToPlayer() - send message back to clients
	def sendMsgToPlayer(self, msgContent):
		pass

	# prepNotification() - prepare notification message (send to clients)
	def prepNotification(self, typeNotify, onObject):
		prepMsg = ""

		# typeNotify is True -> Success Notification

		# typeNotify is False -> Failure Notification

		return prepMsg