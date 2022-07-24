import socket
import threading
import random
import time

SERVER = 'localhost'
PORT = 1234
# CHANGE THIS NUMBER TO # OF CLIENTS YOU WANT RUNNING
NUM_PLAYERS = 4
# may have to adjust buf size
BUF_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((SERVER, PORT))
except socket.error as exc:
    str(exc)

sock.listen(NUM_PLAYERS)

egg_count = 0
egg_coords = []


def threaded_eggs():
    global egg_count
    max_eggs = 10
    while True:
        if egg_count != max_eggs:
            pos = (random.randint(0, 600), random.randint(0, 600))
            egg_coords.append(pos)
            egg_count += 1
            time.sleep(0.5)
            print(egg_coords)
        else:
            time.sleep(1)


def read_coords(coords):
    coords = coords.split(",")
    return int(coords[0]), int(coords[1])


def make_coords(coords):
    return str(coords[0]) + "," + str(coords[1])


def send_coords(coords):
    str = ""
    for coord in coords:
        str += make_coords(coord) + "|"

    return str[:-1]


player_count = 0
ready_count = 0
mouse_coords = [(0, 0), (0, 0), (0, 0), (0, 0)]

def threaded_client(conn, player_num):
    global ready_count, player_count
    conn.send(str.encode(str(player_num)))
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


threading.Thread(target=threaded_eggs, args=()).start()

while True:
    print("Waiting...")
    conn, addr = sock.accept()
    print("Connected: ", addr)

    threading.Thread(target=threaded_client, args=(conn, player_count)).start()
    player_count += 1