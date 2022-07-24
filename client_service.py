import socket

SERVER = 'localhost'
PORT = 1234
BUF_SIZE = 1024

class ClientService:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER
        self.port = PORT
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(BUF_SIZE).decode()
        except socket.error as exc:
            print(exc)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(BUF_SIZE).decode()
        except socket.error as exc:
            print(exc)