import eggMaster
import playerMaster
import server_TCP
import socket
import json

#Socket setup
SERVERADDRESS = "127.0.0.1"
SERVERPORT = 16543
SERVERBUF_SIZE = 2098
FORMAT = "json"
MAX_NUM_PLAYERS = 2
CONNECTED_PLAYERS = 0

#Egg setup
DICT_EGGS_OBJ = {}
PLAYER_THREAD = []
GAME_LIVE = True

class SimpleObj:
	countryName = ""
	continentName = ""

	def __init__(self, country, continent):
		self.countryName = country
		self.continentName = continent

def decodeMsgToObject(userMsg):
	decodeMsg = json.loads(userMsg)

	# if decodeMsg['OBJECTTYPE'] =="Egg":
	# 	decodeMsg['DATA'] = json.loads(decodeMsg["DATA"])
	return decodeMsg

def testDecodeJson():
	jsonMsg = '{"REQUESTTYPE": "data", "OBJECTTYPE": "Egg", "DATA": "{"xCoordinate": "1","yCoordinate": "2"}"}'
	loadMsg = decodeMsgToObject(jsonMsg)
	print(loadMsg['REQUESTTYPE'])
	print(loadMsg['OBJECTTYPE'])
	print(loadMsg['DATA'])

def testServer_TCPClass():
	print("Work outside")
	server = server_TCP.ServerRoom(SERVERADDRESS, SERVERPORT, SERVERBUF_SIZE, MAX_NUM_PLAYERS)
	server.start()
	return None


def main(): 
	# testServer_TCPClass()
	# for threads in PLAYER_THREAD:
	# 	threads.join()
	testDecodeJson()
	return None


if __name__ == "__main__":
	main()