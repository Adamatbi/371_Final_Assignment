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
    THREAD_EGG = None

    # Properties from program_master
    EGG_SEM = threading.Semaphore()

    # CHANGE THIS NUMBER TO # OF CLIENTS YOU WANT RUNNING
    MAX_PLAYERS = 2

    EGG_COORDS = []
    locked_eggs = {}
    MAX_EGGS = 20
    HOLD_TIME = 2

    player_count = 0
    ready_count = 0
    player_scores = [0] * NUM_PLAYERS
    mouse_coords = [(0,0)] * NUM_PLAYERS


    #----------------------------------------------------
    # GENERAL_ADMIN FUNCTIONS
    #----------------------------------------------------

    # __init__() - When initiate the Server -> allow to modify the Properties
    def __init__(self, serverAddress, serverPort, bufferSize, maxPlayers,
        maxEggs, holdTime):
        threading.Thread.__init__(self)
        self.SERVERSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVERADDRESS = serverAddress
        self.SERVERPORT = serverPort
        self.SERVERBUF_SIZE = bufferSize
        self.MAX_PLAYERS = maxNumPlayers
        self.MAX_EGG = maxEggs
        self.HOLD_TIME = holdTime

    # run() - start the object
    def run(self):

        # setup the eggAdmin thread 
        self.establishEggAdminThread()

        # wait & setup the connection to each Player
        self.listenToPlayerOnRoom()

        # all player has connect -> start the game
        self.GAME_LIVE[0] = True
        self.EGGADMIN_THREAD.start()

        # start the clock (countdonw to the end game):
        self.countDownTime()       

        # after COUNTDOWN_TIME expired -> send msg to all clients to "STOP" the game
        self.sendMsgToAllPlayer("STOP")

        # calculate the result -> send to all clients


        return None


    #----------------------------------------------------
    # NETWORK MANAGEMENT FUNCTIONS
    #----------------------------------------------------

    # listenToPlayerOnRoom() - accept connection -> add run each connection on a thread
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

        return None

    # establishEggAdminThread() - create the eggAdmin/thread_egg
    def establishThreadEgg(self):
        
        # init the eggAdmin class:
        self.THREAD_EGG = eggMaster.eggAdmin("eggAdmin", "eggAdmin", self.EGG_SEM,
            self.EGG_COORDS, self.MAX_EGG)

        return None

    # CountDownTime() - thread will countdown and notice server to end game
    def countDownTime(self):
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