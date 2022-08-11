import socket
import threading
import json

SERVER_ADDR = '207.23.210.122'
SERVER_PORT = 1234
# may have to adjust buf size
BUF_SIZE = 1024


class ClientService(threading.Thread):
    coordinates = {
        "eggs_coords": [],
        "locked_coords": [],
        "mouse_coords": []
    }

    def run(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER_ADDR
        self.port = SERVER_PORT
        self.addr = (self.server, self.port)
        self.bufSize = BUF_SIZE
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(self.bufSize).decode()
        except socket.error as exc:
            print(exc)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(self.bufSize).decode()
        except socket.error as exc:
            print(exc)

    def updateCoordinates(self, coords):
        self.coordinates = json.loads(coords)

    def extractCoordinates(self, key):
        return self.coordinates[key]
