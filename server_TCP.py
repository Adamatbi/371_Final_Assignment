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
    #PROPERTIES
    #----------------------------------------------------
    #ServerRoom's configuratio - The default configuration
    SERVERSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVERADDRESS = "127.1.1.1"
    SERVERPORT = 1234
    SERVERBUF_SIZE = 1024
    MAX_NUM_PLAYERS = 4
    
    #User_Management information & Data 
    CONNECTED_PLAYERS = 0
    READY_PLAYERS = 0
    LST_PLAYER_THREAD = {}              # Dictionary of user info: key - PlayerID | value: Address & Port Number

    #Gameplay Information & Data
    DICT_EGGS_OBJ = {}                  # Dictionary of eggs object: key - eggs's coordinate | value: the egg objects




    #----------------------------------------------------
    #GENERAL_ADMIN FUNCTIONS
    #----------------------------------------------------

    #__init__() - The constructor of class Server
    #input: serverName
    def __init__(self, serverAddress, serverPort, bufferSize, maxNumPlayers):
        self.SERVERADDRESS = serverAddress
        self.SERVERPORT = serverPort
        self.SERVERBUF_SIZE = bufferSize
        self.MAX_NUM_PLAYERS = maxNumPlayers

    #sendInvitationToRoom() - allow the host to send his/her address & port number (of the room) to the client
    #this is one time message - user's have to trigger manually each time
    def sendInvitationToJoinRoom(self, clientAddress, clientPortNumber):
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.sendto(bytes(self.SERVERADDRESS & ";" & self.SERVERPORT),(clientAddress, clientPortNumber))
        return None

    #AddNewPlayer - for each new player, increase number of connected players by 1
    def AddNewPlayer(self, playerConnection, playerAddress):
        #Create & start the thread for each client's communication:
        playerThread = threading.Thread(target= self.handlePlayerThread, args=(playerConnection, playerAddress))
        
        #Start the player thread:
        playerThread.start()
        
        #Add player thread to thread list for future calls - key is playerAddress | value is playerThread
        self.LST_PLAYER_THREAD[playerAddress] = playerThread
        return 1



    #----------------------------------------------------
    #NETWORK_ADMIN FUNCTIONS
    #----------------------------------------------------
    #serverBinding() - establish the server on local host, bind and listen on the port
    #also store the thread object (of each player) into LST_PLAYER_THREAD
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
            print("Player {} has started".format(self.LST_PLAYER_THREAD[NewAddress].getName()))
        
        return None       
    
    #
    def handlePlayerThread(self, clientConnection, clientAddress):
        print("This is the new thread for {}".format(clientAddress))
        return
            

"""

def threaded_client(conn, player_num):
    global ready_count, player_count
    conn.send(str.encode("Connection established"))
    conn.recv(BUF_SIZE)
    ready_count += 1
 
    # busy wait -- there is definitely a better solution
    # or just remove the feature of waiting for everyone to join
    while ready_count != NUM_PLAYERS:
        pass

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
            # protocols for client info
            if msg == "MOUSE":
                # sends clients other clients cursor coordinates
                conn.send(str.encode("ready for coords from player " + str(player_num)))
                data = conn.recv(BUF_SIZE)
                coords = read_coords(data.decode())
                mouse_coords[player_num] = coords
                conn.send(str.encode(send_coords(mouse_coords)))

            # sends all clients egg coordinates
            elif msg == "EGG":
                conn.send(str.encode(send_coords(egg_coords)))

    print("Connection lost...")
    conn.close()
"""
