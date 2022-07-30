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
import playerMaster
import eggMaster
import egg

#Class ServerRoom:
class ServerRoom(threading.Thread):
    #----------------------------------------------------
    # PROPERTIES
    #----------------------------------------------------

    # ServerRoom's configuration - The default configuration
    SERVERSOCK = None
    SERVERADDRESS = "127.1.1.1"
    SERVERPORT = 1234
    SERVERBUF_SIZE = 1024
    FORMAT = "json"
    MAX_NUM_PLAYERS = 4
    
    # User_Management information & Data 
    CONNECTED_PLAYERS = 0
    READY_PLAYERS = 0
    GAME_LIVE = False
    PLAYER_RESULT = {}                # Dictionary of user info: key - PlayerID | value: Address & Port Number
    PLAYER_THREAD = {}              # Dictionary of Player
    OTHER_THREAD = []               # List of other thread
    MUTEX = threading.Lock()        # mutex for locking access to UNHATCHED

    # Gameplay Information & Data
    MAX_EGGS = 20

    # Dictionary of eggs object: key - eggs's coordinate | value: the egg objects
    # New Eggs will be added to the dictionary - UNHATCHED
    # HATCHED-> Calculate final score -> store in PLAYER_SUMMARY 
    UNHATCHED = {}       
    HATCHED = []

    # Dictionary of players: key - playerID | value: players' score
    PLAYER_SUMMARY = []


    #----------------------------------------------------
    # GENERAL_ADMIN FUNCTIONS
    #----------------------------------------------------

    # __init__() - The constructor of class Server
    def __init__(self, serverAddress, serverPort, bufferSize, maxNumPlayers):
        threading.Thread.__init__(self)
        self.SERVERSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVERADDRESS = serverAddress
        self.SERVERPORT = serverPort
        self.SERVERBUF_SIZE = bufferSize
        self.MAX_NUM_PLAYERS = maxNumPlayers

    # run() - start the object
    def run(self):
        self.GAME_LIVE = True

        # setup the connection 
        self.listenToPlayerOnRoom()
        print("Work")
        return None



    #----------------------------------------------------
    # NETWORK MANAGEMENT FUNCTIONS
    #----------------------------------------------------

    # listenToPlayerOnRoom() - accept player connection and create playerAdmin thread for each plaeyr
    def listenToPlayerOnRoom(self):

        # try to setup
        try:
            self.SERVERSOCK.bind((self.SERVERADDRESS, self.SERVERPORT))
        except socket.error as socketSetupError:
            str(socketSetupError)

        # listen to until achieve maximum number of player
        self.SERVERSOCK.listen(self.MAX_NUM_PLAYERS)
        print(self.CONNECTED_PLAYERS)
        print("Server is Up")

        # while until all connect
        while self.CONNECTED_PLAYERS < self. MAX_NUM_PLAYERS:

            # accept client connection
            clientSock, clientAddress = self.SERVERSOCK.accept()
            print("{} has connected".format(clientAddress))

            # add player to the PLAYER_RESULT dictionary:
            self.PLAYER_RESULT[clientAddress] = 0

            # add player thread to the PLAYER_THREAD dictionary:
            playerThread = playerMaster.playerAdmin(clientAddress, "player" + str(self.CONNECTED_PLAYERS), clientSock,
                4096, self.UNHATCHED, self.MUTEX)

            # add player to PLAYER_THREAD
            self.PLAYER_THREAD[clientAddress] = playerThread

            # send welcome message
            self.sendMsgToSinglePlayer(clientAddress, "Welcome {}".format(self.PLAYER_THREAD[clientAddress].threadID))

            # Trigger the thread
            playerThread.start()
            self.CONNECTED_PLAYERS += 1
        return None

    # sendMsgToAllPlayer() - send message to all the clients via playerAdmin
    def sendMsgToAllPlayer(self, msgContent):

        # loop through all the players in PLAYER_THREAD -> send message
        for key in self.PLAYER_THREAD:
            self.PLAYER_THREAD[key].sendMsgToPlayer(msgContent)
        return None

    # sendMsgToSinglePlayer() - send message to a particular players via playerAdmin
    def sendMsgToSinglePlayer(self, playerAdress, msgContent):
        # extract a particular player from PLAYER_THREAD by using address
        self.PLAYER_THREAD[playerAdress].sendMsgToPlayer(msgContent)
        return None

    # establishEggAdminThread() - create the eggAdmin which manage the egg object
    def establishEggAdminThread(self):
        pass


    # sendInvitationToRoom() - allow the host to send his/her address & port number (of the room) to the client
    #this is one time message - user's have to trigger manually each time
    def sendInvitationToJoinRoom(self, clientAddress, clientPortNumber):
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.sendto(bytes(self.SERVERADDRESS & ";" & self.SERVERPORT),(clientAddress, clientPortNumber))
        return None

    # convertMsgToJson() - convert the message to json format
    def convertMsgToJson(self):
        pass

    # convertObjectToJson() - convert an object to message in json format
    def convertObjectToJson(self, anyObject):
        pass



    #----------------------------------------------------
    # READ/WRITE WITH MUTEX FUNCTIONS
    #----------------------------------------------------


    # # serverBinding() - establish the server on local host, bind and listen on the port
    # # also store the thread object (of each player) into LST_PLAYER_THREAD
    # def establishConnectOnRoom(self):
    #     try:
    #         self.SERVERSOCK.bind((self.SERVERADDRESS, self.SERVERPORT))
    #     except socket.error as socketSetupError:
    #         str(socketSetupError)

    #     #listen on the port & address
    #     self.SERVERSOCK.listen(self.MAX_NUM_PLAYERS)

    #     #Establish the room - waiting until all players connection to the room
    #     while self.CONNECTED_PLAYERS < self.MAX_NUM_PLAYERS:
    #         #Accept the new connection - connection has been limited to MAX_NUM_PLAYERS
    #         NewConnection, NewAddress = self.SERVERSOCK.accept()

    #         #Create new thread with connection & address -> add to the list of thread & increse CONNECTED_PLAYERS
    #         self.CONNECTED_PLAYERS += self.AddNewPlayer(NewConnection, NewAddress)

    #         #Send confirmation message to the client/player
    #         NewConnection.send(bytes("Player {}".format(NewAddress),"utf-8"))
            
    #         #Print confirmation message on the server's screen
    #         print("{} has started".format(self.PLAYER_THREAD[NewAddress].getName()))
    #     return None

