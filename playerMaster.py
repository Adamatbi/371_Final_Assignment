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

	# Constructor
	def __init__(self, clientAddress, threadName, clientSocket, clientSocketThread,
		bufferSize, eggCoords, lockedEggs):
		threading.Thread.__init__(self)
		self.threadID = clientAddress			# use clientAddress as threadID
		self.name = threadName
		self.CLIENTSOCKET = clientSocket
		self.PLAYER_THREAD = clientSocketThread 
		self.BUF_SIZE = bufferSize
		self.EGG_COORDS = eggCoords
		self.LOCKED_EGGS = lockedEggs


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
				# Store the message -> allow to process the next one
				self.LAST_MSG = msgData
				print("{}: {}".format(self.threadID, self.LAST_MSG))

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
	                conn.send(str.encode(str(program_master.get_scores())))

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


	def check_coords(self, msg, player, egg_count):
	    
	    # format the string into tuple of ints
	    click_coord = self.extractCoordinate(msg)

	    #acquire semaphore
	    self.EGG_SEM.acquire

	    # check clicked if in locked_egg
	    if click_coords in egg_coords:
	    	egg_coords.remove(click_coords)

	    	# lock the egg
	    	self.locked_eggs[player] = click_coords
	    	self.EGG_COUNT -= 1


	    # acquire semaphore
	    self.EGG_SEM.acquire()

	    # if clicked an egg
	    if click_coords in egg_coords:
	        egg_coords.remove(click_coords)

	        # lock the egg
	        locked_eggs[player] = click_coords
	        egg_count -= 1

	        EGG_SEM.release()
	        return True
	    # if did not click an egg
	    else:
	        EGG_SEM.release()
	        return False
	    
	# upon mouse release, check if player successfully got egg
	def validate(self, msg, player, elapsed):
	    
	    # extract infor from msg
	    click_coords = self.extractCoordinate(msg)
	    print(msg)
	    print(player)
	    print(elapsed)

	    # if valid
	    EGG_SEM.acquire()
	    if float(elapsed) >= HOLD_TIME and locked_eggs[player] == click_coords:
	        locked_eggs.pop(player)
	        EGG_SEM.release()
	        return True
	    else:
	        egg_coords.append(locked_eggs[player])
	        locked_eggs.pop(player)
	        EGG_SEM.release()
	        return False

	def inc_score(player_num):
	    player_scores[player_num] += 1


	def get_scores():
	    return player_scores

	def get_locked():
	    return dict.values(locked_eggs)