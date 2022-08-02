import socket
import threading
import time
import random

import program_master

SERVER = 'localhost'
PORT = 1234
# may have to adjust buf size
BUF_SIZE = 1024
ENDTIME = 10
PLAYER_THREAD = []
class Server(threading.Thread):
    coordinates = {
        "eggs_coords": [],
        "locked_coords": [],
        "mouse_coords": []
    }

    def run(self):
        global ENDTIME
        GAME_LIVE = True
        threading.Thread.__init__(self)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((SERVER, PORT))
        except socket.error as exc:
            str(exc)

        sock.listen(program_master.NUM_PLAYERS)
        
        while program_master.player_count != program_master.NUM_PLAYERS:
            print("Waiting...")
            conn, addr = sock.accept()
            print("Connected: ", addr)
            PLAYER_THREAD.append(threading.Thread(target=client_handler, args=(conn, program_master.player_count, lambda: GAME_LIVE)))
            PLAYER_THREAD[-1].start()
            program_master.player_count += 1

        threadegg = threading.Thread(target=program_master.threaded_eggs)
        threadegg.daemon = True
        threadegg.start()

        # clock to end game
        clockCount()
        GAME_LIVE = False

        for player in PLAYER_THREAD:
            player.join()
        return None


def client_handler(conn, player_num, gameLive):
    conn.send(str.encode("Connection established"))
    conn.recv(BUF_SIZE)
    program_master.ready_count += 1
 
    # busy wait -- there is definitely a better solution
    # or just remove the feature of waiting for everyone to join
    while program_master.ready_count != program_master.NUM_PLAYERS:
        time.sleep(0.5)

    # assigns player num, client uses to determine other clients data
    conn.send(str.encode(str(player_num)))
    while True:
        data = conn.recv(BUF_SIZE)
        msg = data.decode()

        if gameLive() == False:
            break

        # if someone leaves, make room for another person to join
        # could probably be handled better -- quite buggy atm
        if not data:
            print("Disconnecting...")
            program_master.ready_count -= 1
            program_master.player_count -= 1 
            break
        else:
            # protocols for client info
            if msg == "ISEND":
                conn.send(str.encode("NO"))
            elif msg == "READY":
                conn.send(str.encode(str(player_num)))
            elif msg == "NUM":
                conn.send(str.encode(str(program_master.NUM_PLAYERS)))
            elif msg == "MOUSE":
                # sends clients other clients cursor coordinates
                conn.send(str.encode("ready for coords from player " + str(player_num)))
                data = conn.recv(BUF_SIZE)
                coords = program_master.read_coords(data.decode())
                program_master.mouse_coords[player_num] = coords
                conn.send(str.encode(program_master.encode_coords(program_master.mouse_coords,"mouse")))

            # sends all clients egg coordinates
            elif msg == "EGG":
                conn.send(str.encode(program_master.encode_coords(program_master.egg_coords,'egg')))

            # sends all clients locked egg coordinates
            elif msg == "LOCKED":
                locked_eggs = list(program_master.get_locked())
                conn.send(str.encode(program_master.encode_coords(locked_eggs,'locked')))
            
            # sends the players scores
            elif msg == "SCORES":
                conn.send(str.encode(str(program_master.get_scores())))

            elif msg == "INC_SCORE":
                program_master.inc_score(player_num)
                conn.send(str.encode(f"increased score of player {player_num+1}"))

            # received a pair of coords to validate
            elif msg[0] == "V":
                print(msg)
                msg = msg[1:]
                msg = msg.split(':')
                if program_master.validate(msg[0], player_num, msg[1]):
                    conn.send(str.encode("true"))
                else:
                    conn.send(str.encode("false"))

            # a player clicked, check if on egg
            else:
                # check if msg in egg coords:
                if program_master.check_coords(msg, player_num):
                    conn.send(str.encode("clicked"))
                else:
                    conn.send(str.encode("missed"))
    print("Connection lost...")
    conn.close()

def clockCount():
    global ENDTIME
    while ENDTIME:
        time.sleep(1)
        ENDTIME -= 1
        print(ENDTIME)
    return None