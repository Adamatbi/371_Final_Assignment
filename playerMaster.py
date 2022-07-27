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
	# eggHolding - keep the egg object that players is currently working on
	EGGHOLDING = None
	CLIENTSOCKET = None
	CLIENTADDRESS = None
	BUF_SIZE = 1024
	DICT_EGG = None

	# Constructor
	def __init__(self, threadID, threadName, clientSocket, clientAddress, bufferSize, dictEggObj):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = threadName
		self.CLIENTSOCKET = clientSocket
		self.CLIENTADDRESS = clientAddress 
		self.BUF_SIZE = bufferSize
		self.DICT_EGG = dictEggObj

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
				break

			# valid request:
			else:
				print("{}: {}".format(self.threadID, msgData))

		return None	


	# # handleClientCommunication() - this will be a separate thread for each clients connect to server
 #    def handleClientCommunication(conn, player_num):
 #        global ready_count, player_count
 #        conn.send(str.encode("Connection established"))
 #        conn.recv(BUF_SIZE)
 #        ready_count += 1
     
 #        # busy wait -- there is definitely a better solution
 #        # or just remove the feature of waiting for everyone to join
 #        while self.READY_PLAYERS != self.CONNECTED_PLAYERS:
 #            time.sleep(0.5)

 #        # assigns player num, client uses to determine other clients data
 #        conn.send(str.encode(str(player_num)))

 #        while True:
 #            data = conn.recv(BUF_SIZE)
 #            msg = data.decode()
            
 #            # if someone leaves, make room for another person to join
 #            # could probably be handled better -- quite buggy atm
 #            if not data:
 #                print("Disconnecting...")
 #                ready_count -= 1
 #                player_count -= 1 
 #                break
 #            else:
 #                ##### This part need to be reviewed ######
 #                # protocols for client info
 #                if msg == "MOUSE":
 #                    # sends clients other clients cursor coordinates
 #                    conn.send(str.encode("ready for coords from player " + str(player_num)))
 #                    data = conn.recv(BUF_SIZE)
 #                    coords = read_coords(data.decode())
 #                    mouse_coords[player_num] = coords
 #                    conn.send(str.encode(encode_coords(mouse_coords,"mouse")))

 #                # sends all clients egg coordinates
 #                elif msg == "EGG":
 #                    conn.send(str.encode(encode_coords(egg_coords,'egg')))

 #        print("Connection lost...")
 #        conn.close()	