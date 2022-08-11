import socket
import threading
import json

SERVER_ADDR = 'localhost'
SERVER_PORT = 1234
# may have to adjust buf size
BUF_SIZE = 1024


class ClientService(threading.Thread):
    coordinates = {
        "eggs_coords": [],
        "locked_coords": [],
        "mouse_coords": []
    }

    #initializes variables and connects to server.
    def run(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER_ADDR
        self.port = SERVER_PORT
        self.addr = (self.server, self.port)
        self.bufSize = BUF_SIZE
        self.id = self.connect()
        print(self.id)

    #create tcp connection with server
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(self.bufSize).decode()
        except socket.error as exc:
            print(exc)

    #encode and send data packet to server
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(self.bufSize).decode()
        except socket.error as exc:
            print(exc)

    #update coordinates from server
    def updateCoordinates(self, coords):
        self.coordinates = json.loads(coords)

    #return coordinates value from internal state
    def extractCoordinates(self, key):
        return self.coordinates[key]
