import socket
import threading
import random
import time
import json

SERVER = 'localhost'
PORT = 1234
# CHANGE THIS NUMBER TO # OF CLIENTS YOU WANT RUNNING
NUM_PLAYERS = 1
# may have to adjust buf size
BUF_SIZE = 1024

global game_live
game_live = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((SERVER, PORT))
except socket.error as exc:
    str(exc)

sock.listen(NUM_PLAYERS)

egg_count = 0
egg_coords = []

player_count = 0
ready_count = 0
mouse_coords = [(0,0)] * NUM_PLAYERS


def generate_egg_position():
    return (random.randint(0, 7)*100, random.randint(0, 7)*100)

def threaded_eggs():
    global egg_count
    max_eggs = 20
    while True:
        if egg_count != max_eggs:
            if random.random()>0.5 and game_live:

                pos = generate_egg_position()
                while pos in egg_coords:
                    pos = generate_egg_position()

               
                egg_coords.append(pos)
                egg_count += 1
            time.sleep(1)
        else:
            time.sleep(1)
    

def read_coords(coords):
    data_dic = json.loads(coords)
    
    return int(data_dic['mouse_coords'][0][0]), int(data_dic['mouse_coords'][0][1])

def encode_coords(coords,coord_type):
    #returns json string of the form {"mouse_coords": [(player_1_x,player_1_y),(player_2_x,player_2_y),ect...]}
    coords_list = list()
    for coord in coords:
        coords_list.append((coord[0],coord[1]))
    
    if coord_type == "mouse":
        return json.dumps({"mouse_coords":coords_list})
    if coord_type == "egg":
        return json.dumps({"egg_coords":coords_list})

def threaded_client(conn, player_num):
    global ready_count, player_count
    conn.send(str.encode("Connection established"))
    conn.recv(BUF_SIZE)
    ready_count += 1
 
    # busy wait -- there is definitely a better solution
    # or just remove the feature of waiting for everyone to join
    while ready_count != NUM_PLAYERS:
        time.sleep(0.5)

    global game_live
    game_live = True

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
                conn.send(str.encode(encode_coords(mouse_coords,"mouse")))

            # sends all clients egg coordinates
            elif msg == "EGG":
                conn.send(str.encode(encode_coords(egg_coords,'egg')))
            
            # a player clicked, check if on egg
            else:
                # if msg in egg_coords:
                click_coords = msg.split(',')
                click_coords[0] = ((int(click_coords[0]))//100)*100
                click_coords[1] = ((int(click_coords[1]))//100)*100
                # prob lock mutex here
                if tuple(click_coords) in egg_coords:
                    egg_coords.remove(tuple(click_coords))
                    conn.send(str.encode("clicked"))
                # did not click an egg
                else:
                    conn.send(str.encode("missed"))


    print("Connection lost...")
    conn.close()

threading.Thread(target=threaded_eggs, args=()).start()

while True:
    print("Waiting...")
    conn, addr = sock.accept()
    print("Connected: ", addr)

    threading.Thread(target=threaded_client, args=(conn, player_count)).start()
    player_count += 1


