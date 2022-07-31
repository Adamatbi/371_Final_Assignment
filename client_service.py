import socket
import threading
import json

class ClientService(threading.Thread):
    coordinates = {
        "eggs_coords": [],
        "locked_coords": [],
        "mouse_coords": []
    }

    def __init__(self, server_address, server_port, buffer_size):
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_address
        self.port = server_port
        self.addr = (self.server, self.port)
        self.bufSize = buffer_size
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


