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
class playerAdmin(threading.Thread):
	# default configuration of playerThread
	CLIENTSOCKET = None
	PLAYER_THREAD = None
	BUF_SIZE = 1024
	MUTEX = None

	# Gameplay properties
	EGG_COORDS = None 		
	LOCKED_EGGS = None
	EGG_COUNT = None
	HOLD_TIME = 2
	PLAYER_SCORES = None
	MOUSE_COORDS = None

	# Constructor
	def __init__(self, clientSocket, clientSocketThread, bufferSize, eggCoords,
		lockedEggs, eggCount, holdTime, playerScores, mouseCoords):
		threading.Thread.__init__(self)
		self.CLIENTSOCKET = clientSocket
		self.PLAYER_THREAD = clientSocketThread 
		self.BUF_SIZE = bufferSize
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

				# protocols for client info
	            if msg == "READY":
	                conn.send(str.encode(str(player_num)))

	            elif msg == "NUM":
	                conn.send(str.encode(str(program_master.NUM_PLAYERS)))

	            elif msg == "MOUSE":
	                # sends clients other clients cursor coordinates
	                conn.send(str.encode("ready for coords from player " + str(player_num)))
	                data = conn.recv(BUF_SIZE)
	                coords = program_master.read_coords(data.decode())
	                program_master.mouse_coords[player_num] = coords
	                conn.send(str.encode(program_master.encode_coords(program_master.mouse_coords,"mouse")))

	            # sends all clients egg coordinates
	            elif msg == "EGG":
	                conn.send(str.encode(program_master.encode_coords(program_master.egg_coords,'egg')))

	            # sends all clients locked egg coordinates
	            elif msg == "LOCKED":
	                locked_eggs = list(program_master.get_locked())
	                conn.send(str.encode(program_master.encode_coords(locked_eggs,'locked')))
	            
	            # sends the players scores
	            elif msg == "SCORES":
	                conn.send(str.encode(str(self.get_scores())))

	            elif msg == "INC_SCORE":
	                program_master.inc_score(player_num)
	                conn.send(str.encode(f"increased score of player {player_num+1}"))

	            # received a pair of coords to validate
	            elif msg[0] == "V":
	                print(msg)
	                msg = msg[1:]
	                msg = msg.split(':')
	                if program_master.validate(msg[0], player_num, msg[1]):
	                    conn.send(str.encode("true"))
	                else:
	                    conn.send(str.encode("false"))

	            # a player clicked, check if on egg
	            else:
	                # check if msg in egg coords:
	                if program_master.check_coords(msg, player_num):
	                    conn.send(str.encode("clicked"))
	                else:
	                    conn.send(str.encode("missed"))
		return None

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
    # ULTILITY FUNCTIONS
    #----------------------------------------------------

    def extractCoordinate(self, msg):
        coords = msg.split(',')
        coords[0] = ((int(coords[0]))//100)*100
        coords[1] = ((int(coords[1]))//100)*100
        return tuple(coords)

    def read_coords(self, coords):
        data_dic = json.loads(coords)    
        return int(data_dic['mouse_coords'][0][0]), int(data_dic['mouse_coords'][0][1])


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
        self.EGG_SEM.acquire

        # check clicked if in locked_egg
        if click_coords in self.EGG_COORDS:
            self.EGG_COORDS.remove(click_coords)

            # lock the egg
            self.LOCKED_EGGS[player] = click_coords
            self.EGG_COUNT[0] -= 1
            check = True

        # acquire semaphore
        self.EGG_SEM.acquire()
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
        return self.PLAYER_SCORES

    def get_locked():
        return dict.values(self.LOCKED_EGGS)
