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
    PLAYER_COUNT = 0
    READY_COUNT = 0
    
    EGG_COORDS = []
    LOCKED_EGGS = {}
    MAX_EGGS = 20
    EGG_COUNT = []              # a list object will be pass as reference 
    HOLD_TIME = 2

    GAME_LIVE = [False]
    GAME_TIME = 90
    CURRENT_TIME = 0

    PLAYER_SCORES = [0] * MAX_PLAYERS
    MOUSE_COORDS = [(0,0)] * MAX_PLAYERS


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
        self.EGG_COUNT.append(0)   

    # run() - start the object
    def run(self):

        # setup the eggAdmin thread 
        self.establishEggAdminThread()

        # wait & setup the connection to each Player
        self.listenToPlayerOnRoom()

        # all player has connect -> start the game
        self.GAME_LIVE[0] = True
        self.EGGADMIN_THREAD.start()

        # countDownTime -> keep the game run within allow time -> set GAME_LIVE = False
        self.countDownTime()       

        # after COUNTDOWN_TIME expired -> send msg to all clients to "STOP" the game
        #self.sendMsgToAllPlayer("STOP")

        # calculate the result -> send to all clients

        return None


    #----------------------------------------------------
    # PREPARE ALL THREAD FOR SERVER
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

            # Increase number of connected players
            self.CONNECTED_PLAYERS += 1

            # initiate/add player to playerThread:
            playerThread = playerMaster.playerThread(self.CONNECTED_PLAYERS, clientSocket, 4096, self.MAX_PLAYERS, 
                self.EGG_COORDS, self.LOCKED_EGGS, self.HOLD_TIME, self.PLAYER_SCORES, self.MOUSE_COORDS)

            # send welcome message
            self.sendMsgToSinglePlayer(clientAddress, "Welcome {}".format(self.PLAYER_THREAD[clientAddress].threadID))

            # Trigger the thread
            playerThread.start()
        return None

    # establishEggAdminThread() - create the eggAdmin/thread_egg
    def establishThreadEgg(self):
        # init the eggAdmin class:
        self.THREAD_EGG = eggMaster.eggAdmin("eggAdmin", "eggAdmin", self.EGG_SEM,
            self.EGG_COORDS, self.MAX_EGG, self.EGG_COUNT)

        return None

    # CountDownTime() - thread will countdown and notice server to end game
    def countDownTime(self):
        while self.GAME_LIVE:
            time.sleep(1)
            
            # increase the current time
            self.CURRENT_TIME += 1

            # Time get expired
            if self.CURRENT_TIME == self.GAME_TIME :
                break
        self.GAME_LIVE = False
        return None
