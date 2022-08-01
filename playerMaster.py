"""
Class PlayerThread
- this class is the extension of class Thread
- major task: receiving message from clients, change/update the egg
- to trigger the thread -> playerThread.run() or playerThread.start()
"""
import socket
import threading
import json


# playerThread - child of class Threading 
class playerThread(threading.Thread):
	# default configuration of playerThread
	CLIENTSOCKET = None
	BUF_SIZE = 1024

	# Gameplay properties
	MAX_PLAYERS = 4
	EGG_COORDS = None 		
	LOCKED_EGGS = None
	HOLD_TIME = 2
	EGG_COUNT = None
	PLAYER_SCORES = None 			
	MOUSE_COORDS = None 			

	# Constructor
	def __init__(self, ID, threadName, clientSocket, bufferSize, maxPlayer, eggCoords,
		lockedEggs, eggCount, holdTime, playerScores, mouseCoords):
		threading.Thread.__init__(self)
		self.threadID = ID
		self.CLIENTSOCKET = clientSocket
		self.BUF_SIZE = bufferSize

		self.MAX_PLAYERS = maxPlayer
		self.EGG_COORDS = eggCoords
		self.LOCKED_EGGS = lockedEggs
		self.EGG_COUNT = eggCount
		self.HOLD_TIME = holdTime
		self.PLAYER_SCORES = playerScores
		self.MOUSE_COORDS = mouseCoords


	# run() - main execution of the player thread 
	def run(self):
		# while the game is running -> listen to any update
		while True:
			#listen to any message from client	
			data = self.CLIENTSOCKET.recv(self.BUF_SIZE)
			msg = data.decode("utf_8")

			# Player disconnect from server
			if not msg:
				print("Player {} Disconnecting...".format(self.threadID))
            	return self.threadID

			# valid request:
			else:
				# protocols for client info
				if msg == "READY":
					self.sendMsgToPlayer(self.threadID)

				elif msg == "NUM":
					self.sendMsgToPlayer(self.MAX_PLAYERS)

				elif msg == "MOUSE":
					self.sendMsgToPlayer("ready for coords from player " + str(self.threadID))
					data = conn.recv(self.BUF_SIZE)
					coords = self.read_coords(data.decode("utf_8"))
					self.sendMsgToPlayer(self.encode_coords(self.MOUSE_COORDS, "mouse"))

				# send all client egg coordinates
				elif msg == "EGG":
					self.sendMsgToPlayer(self.encode_coords(self.EGG_COORDS, "egg"))

				# send all clients locked egg coordinates
				elif msg == "LOCKED":
					self.LOCKED_EGGS = list(self.get_locked())
					self.sendMsgToPlayer(self.encode_coords(self.LOCKED_EGGS, 'locked'))

				# send players' score
				elif msg == "SCORES":
					self.sendMsgToPlayer(self.get_scores())

				# increase player score
				elif msg == "INC_SCORE":
					self.inc_score(self.threadID - 1)
					self.sendMsgToPlayer(f"increased score of player {self.threadID}")
				
				# receive a pair of coords to validate
				elif msg[0] == "V":	
					print(msg)
					msg = [1:]
					msg = msg.split(":")
					if self.validate(msg[0], self.threadID, msg[1]):
						self.sendMsgToPlayer("True")
					else:
						self.sendMsgToPlayer("False")

				# a player clicked, check if on egg
				else:
					if self.check_coords(msg, player_num):
						self.sendMsgToPlayer("clicked")
					else:
						self.sendMsgToPlayer("missed")
		return None

    #----------------------------------------------------
    # ULTILITY FUNCTIONS
    #----------------------------------------------------

    # sendMsgToPlayer() - send message back to clients
	def sendMsgToPlayer(self, msgContent):
		self.CLIENTSOCKET.send(bytes(msgContent,"utf-8"))
		return None

	# extract coordinate in the message
    def extractCoordinate(self, msg):
        coords = msg.split(',')
        coords[0] = ((int(coords[0]))//100)*100
        coords[1] = ((int(coords[1]))//100)*100
        return tuple(coords)

    # read coords 
    def read_coords(self, coords):
        data_dic = json.loads(coords)    
        return int(data_dic['mouse_coords'][0][0]), int(data_dic['mouse_coords'][0][1])

    # convert coordinate to json format
    def encode_coords(self, coords, coord_type):
        #returns json string of the form {"mouse_coords": [(player_1_x,player_1_y),(player_2_x,player_2_y),ect...]}
        coords_list = list()
        for coord in coords:
            coords_list.append((coord[0],coord[1]))
        
        return json.dumps({f"{coord_type}_coords":coords_list})

    # check_coords() - function from program_master.py
    def check_coords(self, msg, player, egg_count):
        check = False

        # format the string into tuple of ints
        click_coord = self.extractCoordinate(msg)

        #acquire semaphore
        self.EGG_SEM.acquire()

        # check clicked if in locked_egg
        if click_coords in self.EGG_COORDS:
            self.EGG_COORDS.remove(click_coords)

            # lock the egg
            self.LOCKED_EGGS[player] = click_coords
            self.EGG_COUNT[0] -= 1
            check = True

        # release semaphore
        self.EGG_SEM.release()
        return check
        
    # upon mouse release, check if player successfully got egg
    def validate(self, msg, player, elapsed):
        check = False

        # extract coordinate from message
        click_coords = self.extractCoordinate(msg)

        # acquire semaphore
        self.EGG_SEM.acquire()

        # if valid 
        if float(elapsed) >= self.HOLD_TIME and self.LOCKED_EGGS[player] == click_coords:
            self.LOCKED_EGGS.pop(player)
            check = True

        # not valid
        else:
            self.EGG_COORDS.append(self.LOCKED_EGGS[player])
            self.LOCKED_EGGS.pop(player)
            check = False

        # release semaphore
        self.EGG_SEM.release()

        return check


    def inc_score(player_num):
        self.PLAYER_SCORES[player_num] += 1

    def get_scores():
        return str.encode(self.PLAYER_SCORES)

    def get_locked():
        return dict.values(self.LOCKED_EGGS)
