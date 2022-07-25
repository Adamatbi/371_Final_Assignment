import random
import json
import threading
from typing import Dict

EGG_SEM = threading.Semaphore()

# CHANGE THIS NUMBER TO # OF CLIENTS YOU WANT RUNNING
NUM_PLAYERS = 1

egg_count = 0
egg_coords = []
locked_eggs = {}
MAX_EGGS = 20

player_count = 0
ready_count = 0
player_scores = [0] * NUM_PLAYERS
mouse_coords = [(0,0)] * NUM_PLAYERS

game_live = False

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
    # format the string into tuple of ints
    click_coords = msg.split(',')
    click_coords[0] = ((int(click_coords[0]))//100)*100
    click_coords[1] = ((int(click_coords[1]))//100)*100
    click_coords = tuple(click_coords)
    # acquire semaphore
    EGG_SEM.acquire()
    # if clicked an egg
    if click_coords in egg_coords:
        egg_coords.remove(click_coords)
        # lock the egg
        locked_eggs[player] = click_coords
        # egg_count -= 1
        EGG_SEM.release()
        return True
    # if did not click an egg
    else:
        EGG_SEM.release()
        return False
    
# upon mouse release, check if player successfully got egg
def validate(msg, player):
    click_coords = msg.split(',')
    click_coords[0] = ((int(click_coords[0]))//100)*100
    click_coords[1] = ((int(click_coords[1]))//100)*100
    click_coords = tuple(click_coords)
    
    # if valid
    if locked_eggs[player] == click_coords:
        locked_eggs.pop(player)
        return True
    else:
        egg_coords.append(locked_eggs[player])
        locked_eggs.pop(player)
        return False

def inc_score(player_num):
    player_scores[player_num] += 1


def get_scores():
    return player_scores

def get_locked():
    return dict.values(locked_eggs)