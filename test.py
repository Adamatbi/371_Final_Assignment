import eggMaster
import playerMaster
import socket

#Socket setup
SERVERADDRESS = "127.1.1.1"
SERVERPORT = 1234
SERVERBUF_SIZE = 1024
FORMAT = "json"
MAX_NUM_PLAYERS = 2
CONNECTED_PLAYERS = 0

#Egg setup
DICT_EGGS_OBJ = {}
PLAYER_THREAD = []
GAME_LIVE = True

def testDict():
	eggAdminTest = eggMaster.eggAdmin("Egg1","Admin1", True, DICT_EGGS_OBJ)
	print(eggAdminTest.THREADID)
	print(eggAdminTest.THREADNAME)
	eggAdminTest.run(GAME_LIVE, 10)
	return None

def testSocket():
	serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		serverSock.bind((SERVERADDRESS, SERVERPORT))
	except socket.error as socketSetupError:
		str(socketSetupError)

	serverSock.listen(MAX_NUM_PLAYERS)
	count = 1
	while len(PLAYER_THREAD) < MAX_NUM_PLAYERS:
		print("Server is up")
		print(len(PLAYER_THREAD))
		clientSock, clientAddress = serverSock.accept()
		print("{} has connected".format(clientAddress))
		clientHelper = playerMaster.playerThread(count, "player", clientSock, clientAddress, 4096)
		clientHelper.start()
		PLAYER_THREAD.append(clientHelper)
		count += 1
	return None

def main(): 
	testDict()
	for men in (DICT_EGGS_OBJ):
		print(men.getCoordinate())
	# testSocket()
	# for threads in PLAYER_THREAD:
	# 	threads.join()
	# return None


if __name__ == "__main__":
	main()