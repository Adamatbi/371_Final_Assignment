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
    MAXPLAYER = 2
    
    # User_Management information & Data 
    CONNECTED_PLAYERS = 0
    GAME_LIVE = [False]
    COUNTDOWN_TIME = 180            # The value of COUNTDOWN_TIME will be 180 seconds - 3 minutes
    CURRENT_COUNTDOWN = 0           # Time to count down
    PLAYER_RESULT = {}              # Dictionary of user info: key - PlayerID | value: Address & Port Number
    PLAYER_THREAD = {}              # Dictionary of Player
    EGGADMIN_THREAD = None          # EggAdmin thread -> manage/create/kill all eggs
    MUTEX = threading.Lock()        # mutex for locking access to UNHATCHED

    # Gameplay Information & Data
    MAX_EGG = 20

    # Dictionary of eggs object: key - eggs's coordinate | value: the egg objects
    # New Eggs will be added to the dictionary - UNHATCHED
    # HATCHED-> Calculate final score -> store in PLAYER_SUMMARY 
    UNHATCHED_EGG = {}       
    HATCHED_EGG = []

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
        self.MAXPLAYER = maxNumPlayers

    # run() - start the object
    def run(self):

        # setup the eggAdmin thread 
        self.establishEggAdminThread()

        # wait & setup the connection to each Player
        self.listenToPlayerOnRoom()

        # all player has connect -> start the game
        self.GAME_LIVE[0] = True
        self.EGGADMIN_THREAD.start()

        # start the clock (countdonw to end game):
        threading.Thread(target = self.threadCountDownTimem).start()        

        # after COUNTDOWN_TIME expired -> send msg to all clients to "STOP" the game
        self.sendMsgToAllPlayer("STOP")

        # calculate the result -> send to all clients


        return None


    #----------------------------------------------------
    # NETWORK MANAGEMENT FUNCTIONS
    #----------------------------------------------------

    # listenToPlayerOnRoom() - accept player connection and create playerAdmin thread for each plaeyr
    def listenToPlayerOnRoom(self):

        # listen on channel
        try:
            self.SERVERSOCK.bind((self.SERVERADDRESS, self.SERVERPORT))
        except socket.error as socketSetupError:
            str(socketSetupError)

        # listen to until achieve maximum number of player
        self.SERVERSOCK.listen(self.MAXPLAYER)

        # while until all player connect -> put in PLAYERTHREAD
        while self.CONNECTED_PLAYERS < self.MAXPLAYER:

            # accept client connection
            clientSocket, clientAddress = self.SERVERSOCK.accept()
            print("{} has connected".format(clientAddress))

            # add player to the PLAYER_RESULT dictionary:
            self.PLAYER_RESULT[clientAddress] = 0

            # add player thread to the PLAYER_THREAD dictionary:
            playerThread = playerMaster.playerAdmin(clientAddress, "player" + str(self.CONNECTED_PLAYERS),
                clientSocket, self.PLAYER_THREAD,4096, self.UNHATCHED_EGG, self.MUTEX)

            # add player to PLAYER_THREAD
            self.PLAYER_THREAD[clientAddress] = playerThread

            # send welcome message
            self.sendMsgToSinglePlayer(clientAddress, "Welcome {}".format(self.PLAYER_THREAD[clientAddress].threadID))

            # Trigger the thread
            playerThread.start()

            # Increase number of connected players
            self.CONNECTED_PLAYERS += 1
            print(self.CONNECTED_PLAYERS)

        return None

    # establishEggAdminThread() - create the eggAdmin which manage the egg object
    def establishEggAdminThread(self):
        
        # init the eggAdmin class:
        self.EGGADMIN_THREAD = eggMaster.eggAdmin("eggAdmin", "eggAdmin", self.PLAYER_THREAD,
            self.UNHATCHED_EGG, self.HATCHED_EGG, self.MAX_EGG, self.GAME_LIVE)

        return None

    # threadCountDownTime() - thread will countdown and notice server to end game
    def threadCountDownTime(self):
        while self.GAME_LIVE:
            time.sleep(1)
            
            # increase the current time
            self.CURRENT_COUNTDOWN += 1

            # Time get expired
            if self.CURRENT_COUNTDOWN == self.COUNTDOWN_TIME:
                break
        self.GAME_LIVE = False
        return None

    # calculateFinalResult() - calculate final result return a message to send
    def calculateFinalResult(self):
        pass

    #----------------------------------------------------
    # UTILITY FUNCTIONS
    #----------------------------------------------------

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

