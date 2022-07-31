import socket
import threading
import time

""
class Client():
    CLIENTSOCK = None
    CLIENTADDRESS = "127.0.0.10"
    CLIENTPORT = 12345
    CLIENTBUF_SIZE = 1024
    HOSTADDRESS = ""
    HOSTPORT = 0
    THREAD_RECEV = None
    THREAD_SEND = None
    SERVER_MSG = ""
    USER_MSG = ""

    # Constructor
    def __init__(self, clientAddresss, clientPort, buffer_size) -> None:
        #threading.Thread.__init__(self)
        self.CLIENTSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CLIENTADDRESS = clientAddresss
        self.CLIENTPORT = clientPort
        self.CLIENTBUF_SIZE = buffer_size
        return None

    # requestConnect - establish the connection between host and client
    def requestConnect(self, hostAddress, hostPort):
        self.HOSTADDRESS = hostAddress
        self.HOSTPORT = hostPort
        
        #establish connection to the host socket
        self.CLIENTSOCK.connect((self.HOSTADDRESS, self.HOSTPORT))
        return None

    # sendClientMsg() - send the message to host
    def sendClientMsg(self, userMsg):
        self.CLIENTSOCK.sendall(bytes(userMsg,"utf-8"))
        return None

    # recvHostMsg() - receive message from host
    def recvHostMsg(self):
        while True:
            self.SERVER_MSG = self.CLIENTSOCK.recv(self.CLIENTBUF_SIZE).decode("utf_8")
            print(self.SERVER_MSG)
        return None

    # getUserInput() - receive user input & send to server
    def getUserInput(self):
        while True:
            self.USER_MSG = input("Type: ") 
            self.sendClientMsg(self.USER_MSG)
        return None

    #function for testing - this work now
    def run(self):
        self.requestConnect("127.0.0.1",16543)

        # create non-blocking THREAD_RECEV
        self.THREAD_RECEV = threading.Thread(target= self.recvHostMsg)
        
        # create non-block THREAD_INPUT
        self.THREAD_INPUT = threading.Thread(target = self.getUserInput)

        # trigger both thread
        self.THREAD_RECEV.start()
        self.THREAD_INPUT.start()

        return

def main():
    client1 = Client("127.1.1.2",1234,4096)
    client1.run()
    return

if __name__ == "__main__":
    main()