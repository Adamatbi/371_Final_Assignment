import random
import json
import threading
import time

EGG_SEM = threading.Semaphore()

# CHANGE THIS NUMBER TO # OF CLIENTS YOU WANT RUNNING
NUM_PLAYERS = 4

# current number of available eggs in the game
egg_count = 0
# stores the coordinates of all available eggs in the game
egg_coords = []
# stores the coordinates of all locked eggs in the game
locked_eggs = {}
# maximum number of available eggs that can be in the game at a time
MAX_EGGS = 20
# amount of time user must click the egg for to receive a point
HOLD_TIME = 2

# number of players that are connected
player_count = 0
ready_count = 0
# holds the scores of all players
player_scores = [0] * NUM_PLAYERS
# holds the mouse coordinates of all players
mouse_coords = [(0,0)] * NUM_PLAYERS

# function that generates eggs every 1 second in the background
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

# generates a random coordinate location
def generate_egg_position():
    return (random.randint(0, 7)*100, random.randint(0, 7)*100)

# converts json data to an int tuple
def read_coords(coords):
    data_dic = json.loads(coords)    
    return int(data_dic['mouse_coords'][0][0]), int(data_dic['mouse_coords'][0][1])

# returns json string of the form {"mouse_coords": [(player_1_x,player_1_y),(player_2_x,player_2_y),ect...]}
def encode_coords(coords,coord_type):
    coords_list = list()
    for coord in coords:
        coords_list.append((coord[0],coord[1]))
    return json.dumps({f"{coord_type}_coords":coords_list})

# returns true if player clicked on an available egg, false otherwise
def check_coords(msg, player):
    global egg_count
    check = False
    # format the string into tuple of ints
    click_coords = extractCoordinates(msg)
    # acquire semaphore
    EGG_SEM.acquire()
    # if clicked an available egg
    if click_coords in egg_coords:
        # lock the egg
        egg_coords.remove(click_coords)
        # record which player locked the egg
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
    # for testing purposes
    print(msg)
    print(player)
    print(elapsed)
    EGG_SEM.acquire()
    # check if player has held click for at least the required amount of time and their 
    # cursor is still on top of the egg image
    if float(elapsed) >= HOLD_TIME and locked_eggs[player] == click_coords:
        locked_eggs.pop(player)
        check = True
    # otherwise, unlock the egg and make it available again
    else:
        egg_coords.append(locked_eggs[player])
        locked_eggs.pop(player)
    EGG_SEM.release()
    return check

# return a tuple of ints
def extractCoordinates(msg):
    click_coords = msg.split(',')
    click_coords[0] = ((int(click_coords[0]))//100)*100
    click_coords[1] = ((int(click_coords[1]))//100)*100
    return tuple(click_coords)
    
# increment the player score
def inc_score(player_num):
    player_scores[player_num] += 1

# return player scores
def get_scores():
    return player_scores

# return the cooridnates of all locked eggs
def get_locked():
    return dict.values(locked_eggs)