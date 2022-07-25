"""
server_TCP
Task: Manage the communication between client and server

"""

from distutils.log import error
from os import lstat
import socket
import threading
import random
import time

#user_defined library
import egg

#Class ServerRoom:
class ServerRoom:
    #----------------------------------------------------
    # PROPERTIES
    #----------------------------------------------------

    # ServerRoom's configuratio - The default configuration
    SERVERSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVERADDRESS = "127.1.1.1"
    SERVERPORT = 1234
    SERVERBUF_SIZE = 1024
    MAX_NUM_PLAYERS = 4
    
    # User_Management information & Data 
    CONNECTED_PLAYERS = 0
    READY_PLAYERS = 0
    GAME_LIVE = False
    PLAYER_THREAD = {}              # Dictionary of user info: key - PlayerID | value: Address & Port Number
    OTHER_THREAD = []                   # List of other thread

    # Gameplay Information & Data
    MAX_EGGS = 20
    EGG_COUNT = 0
    # Dictionary of eggs object: key - eggs's coordinate | value: the egg objects
    # New Eggs will be added to the dictionary
    # Loop through Dictionary of eggs -> Sum with PlayerID -> get score for each player -> store in PLAYER_SUMMARY 
    DICT_EGGS_OBJ = {}

    # Stack to store all finished eggs
    STACK_FINISH_EGG = []       

    # Dictionary of players: key - playerID | value: players' score
    PLAYER_SUMMARY = {}


    #----------------------------------------------------
    # GENERAL_ADMIN FUNCTIONS
    #----------------------------------------------------

    # __init__() - The constructor of class Server
    def __init__(self, serverAddress, serverPort, bufferSize, maxNumPlayers):
        self.SERVERADDRESS = serverAddress
        self.SERVERPORT = serverPort
        self.SERVERBUF_SIZE = bufferSize
        self.MAX_NUM_PLAYERS = maxNumPlayers

    # sendInvitationToRoom() - allow the host to send his/her address & port number (of the room) to the client
    #this is one time message - user's have to trigger manually each time
    def sendInvitationToJoinRoom(self, clientAddress, clientPortNumber):
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.sendto(bytes(self.SERVERADDRESS & ";" & self.SERVERPORT),(clientAddress, clientPortNumber))
        return None

    # generateEggPosition() - randomly
    def generateEggPosition(self):
        pos = (-1,-1)
        while pos == (-1,-1) or pos in self.DICT_EGGS_OBJ:    
            pos = (random.randint(0, 7)*100, random.randint(0, 7)*100)
        return pos

    def generateEggsRandomly(self):
        timeToCount = 
        while self.GAME_LIVE:
            time.sleep(1)
            if self.EGG_COUNT < self.MAX_EGGS and random.random() > 0.5:
                pos = self.generateEggPosition()

                # Store Eggs object into DICT_EGGS_OBJ & increase EGG_COUNT
                # EggNode(xCoordinate, yCoordinate, visible, lock, occupy, points)
                self.DICT_EGGS_OBJ[pos] = egg.EggNode(pos[0], pos[1], True, True, True, 1)
                self.EGG_COUNT += 1

    # generateEggs() - if the egg is occupied by players -> remove from DICT_EGGS_OBJ -> move it to STACK_FINISH_EGG
    def collectedEggs(self):
        pass

    # convertMsgToJson() - convert the message to json file
    def convertMsgToJson(self):
        pass


    #----------------------------------------------------
    # NETWORK_ADMIN FUNCTIONS
    #----------------------------------------------------

    # handleClientCommunication() - this will be a separate thread for each clients connect to server
    def handleClientCommunication(conn, player_num):
        global ready_count, player_count
        conn.send(str.encode("Connection established"))
        conn.recv(BUF_SIZE)
        ready_count += 1
     
        # busy wait -- there is definitely a better solution
        # or just remove the feature of waiting for everyone to join
        while self.READY_PLAYERS != self.CONNECTED_PLAYERS:
            time.sleep(0.5)

        # assigns player num, client uses to determine other clients data
        conn.send(str.encode(str(player_num)))

        while True:
            data = conn.recv(BUF_SIZE)
            msg = data.decode()
            
            # if someone leaves, make room for another person to join
            # could probably be handled better -- quite buggy atm
            if not data:
                print("Disconnecting...")
                ready_count -= 1
                player_count -= 1 
                break
            else:
                ##### This part need to be reviewed ######
                # protocols for client info
                if msg == "MOUSE":
                    # sends clients other clients cursor coordinates
                    conn.send(str.encode("ready for coords from player " + str(player_num)))
                    data = conn.recv(BUF_SIZE)
                    coords = read_coords(data.decode())
                    mouse_coords[player_num] = coords
                    conn.send(str.encode(encode_coords(mouse_coords,"mouse")))

                # sends all clients egg coordinates
                elif msg == "EGG":
                    conn.send(str.encode(encode_coords(egg_coords,'egg')))

        print("Connection lost...")
        conn.close()


    # addNewPlayer() - for each new player, increase number of connected players by 1
    def addNewPlayer(self, playerConnection, playerAddress):
        #Create & start the thread for each client's communication:
        playerThread = threading.Thread(target= self.handleClientCommunication, args=(playerConnection, playerAddress))
        
        #Start the player thread:
        playerThread.start()
        
        #Add player thread to thread list for future calls - key is playerAddress | value is playerThread
        self.PLAYER_THREAD[playerAddress] = playerThread
        return 1


    # serverBinding() - establish the server on local host, bind and listen on the port
    # also store the thread object (of each player) into LST_PLAYER_THREAD
    def establishConnectOnRoom(self):
        try:
            self.SERVERSOCK.bind((self.SERVERADDRESS, self.SERVERPORT))
        except socket.error as socketSetupError:
            str(socketSetupError)

        #listen on the port & address
        self.SERVERSOCK.listen(self.MAX_NUM_PLAYERS)

        #Establish the room - waiting until all players connection to the room
        while self.CONNECTED_PLAYERS < self.MAX_NUM_PLAYERS:
            #Accept the new connection - connection has been limited to MAX_NUM_PLAYERS
            NewConnection, NewAddress = self.SERVERSOCK.accept()

            #Create new thread with connection & address -> add to the list of thread & increse CONNECTED_PLAYERS
            self.CONNECTED_PLAYERS += self.AddNewPlayer(NewConnection, NewAddress)

            #Send confirmation message to the client/player
            NewConnection.send(bytes("Player {}".format(NewAddress),"utf-8"))
            
            #Print confirmation message on the server's screen
            print("{} has started".format(self.PLAYER_THREAD[NewAddress].getName()))
        return None

    # startTheGame() - after all players in "Ready" mode -> the host can click "Start" to trigger the game
    def startTheGame(self):
        # While the game is running 
        while self.GAME_LIVE:
            # Constanly Listening message


            # Sending Message if any update

        pass

    # endTheGame() - join all threads in PLAYER_THREAD & OTHER_THREAD
    def endTheGame(self):

        # send the final score to all players


        # kill PLAYER_THREAD 
        for threads in self.PLAYER_THREAD:
            self.PLAYER_THREAD[threads].join()

        # kill OTHER_THREAD
        for threads in self.OTHER_THREAD:
            self.OTHER_THREAD[threads].join()

        return None
    