import random
import json
import threading
import time

EGG_SEM = threading.Semaphore()

# CHANGE THIS NUMBER TO # OF CLIENTS YOU WANT RUNNING
NUM_PLAYERS = 2

egg_count = 0
egg_coords = []
locked_eggs = {}
MAX_EGGS = 20
HOLD_TIME = 2

player_count = 0
ready_count = 0
player_scores = [0] * NUM_PLAYERS
mouse_coords = [(0,0)] * NUM_PLAYERS

def threaded_eggs():
    global egg_count
    while True:
        if egg_count != MAX_EGGS:
            # generate eggs
            pos = generate_egg_position()
            # acquire semaphore
            EGG_SEM.acquire()
            # generate coordinates for new egg that are not already taken
            while pos in egg_coords:
                pos = generate_egg_position()
            # add new egg to list of eggs
            egg_coords.append(pos)
            egg_count += 1
            print(pos)
            # release semaphore
            EGG_SEM.release()
        else:
            print('max eggs reached')

        time.sleep(1)


def generate_egg_position():
    return (random.randint(0, 7)*100, random.randint(0, 7)*100)


def read_coords(coords):
    data_dic = json.loads(coords)    
    return int(data_dic['mouse_coords'][0][0]), int(data_dic['mouse_coords'][0][1])


def encode_coords(coords,coord_type):
    #returns json string of the form {"mouse_coords": [(player_1_x,player_1_y),(player_2_x,player_2_y),ect...]}
    coords_list = list()
    for coord in coords:
        coords_list.append((coord[0],coord[1]))
    
    return json.dumps({f"{coord_type}_coords":coords_list})


def check_coords(msg, player):
    global egg_count
    check = False
    # format the string into tuple of ints
    click_coords = extractCoordinates(msg)

    # acquire semaphore
    EGG_SEM.acquire()
    # if clicked an egg
    if click_coords in egg_coords:
        egg_coords.remove(click_coords)
        # lock the egg
        locked_eggs[player] = click_coords
        egg_count -= 1
        check = True
    # if did not click an egg
    
    EGG_SEM.release()
    return check
    
# upon mouse release, check if player successfully got egg
def validate(msg, player, elapsed):
    check = False
    click_coords = extractCoordinates(msg)
    print(msg)
    print(player)
    print(elapsed)
    # if valid
    EGG_SEM.acquire()
    if float(elapsed) >= HOLD_TIME and locked_eggs[player] == click_coords:
        locked_eggs.pop(player)
        check = True
    else:
        egg_coords.append(locked_eggs[player])
        locked_eggs.pop(player)
    
    EGG_SEM.release()
    return check

def extractCoordinates(msg):
    click_coords = msg.split(',')
    click_coords[0] = ((int(click_coords[0]))//100)*100
    click_coords[1] = ((int(click_coords[1]))//100)*100
    return tuple(click_coords)
    

def inc_score(player_num):
    player_scores[player_num] += 1


def get_scores():
    return player_scores

def get_locked():
    return dict.values(locked_eggs)