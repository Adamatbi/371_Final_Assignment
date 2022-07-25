import random

import pygame
import os
import json
import time

from client_service import ClientService
import program_master

# Initialize the pygame
pygame.init()

# Create the window and clock
width = 700
height = 700
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Caption
pygame.display.set_caption("Easter Egg Game")

# Backgroud and Image
easterbg = pygame.transform.scale(pygame.image.load(os.path.join("img", "easterbg.jpg")), (width, height))
easteregg = pygame.transform.scale(pygame.image.load(os.path.join("img", "easteregg.png")), (100, 100))
easteregglocked = pygame.transform.scale(pygame.image.load(os.path.join("img", "easteregglocked.png")), (100, 100))

# Player Cursors
cursors = [None] * program_master.NUM_PLAYERS
for i in range(0, program_master.NUM_PLAYERS):
    cursors[i] = pygame.transform.scale(pygame.image.load(os.path.join("img", f"p{i+1}.png")), (50, 50))
player_num = -1

# Font
font100 = pygame.font.SysFont("comics", 100)
font60 = pygame.font.SysFont("comics", 60)
font30 = pygame.font.SysFont("comics", 20)

# Color
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

service = ClientService()
# Easy to calculate position (Temporary)
# test = pygame.transform.scale(pygame.image.load(os.path.join("img", "test.png")), (700, 700))

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    win.blit(img, (x, y))

def main():
    run = True
    win.fill(white)
    # countdown = 10
    last_count = pygame.time.get_ticks()
    pygame.mouse.set_visible(False)

    click_flag = False
    timer = 0
    
    while run:
        
        clock.tick(60)
        win.fill(white)
        egg_handler()
        mouse_handler()
        # print player scores
        scores = service.send("SCORES")
        scores = scores[1:-1]
        scores = scores.split(', ')
        print(scores)
        for i in range(0, program_master.NUM_PLAYERS):
            draw_text(f"Player {i+1} Score: {scores[i]}", font30, black, i*200, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # send pos to server
                reply = service.send(','.join(map(str, pos)))
                # server will have database for positions of eggs
                # if pos is in certain range (we have to choose), server will give a score to the player
                print(reply)
                if reply == 'clicked':
                    click_flag = True
                    timer = time.time()
                    # timer = time.ctime()
                    # while pygame.mouse.get_pressed()==(1,0,0):
                    #     print("mouse is clicked!!")
                    
                    # time_elapsed = time.ctime() - timer
                    # if time_elapsed >= 5 and pos == pygame.mouse.get_pos():
                    
            elif click_flag and event.type == pygame.MOUSEBUTTONUP:
                elapsed = time.time() - timer
                click_flag = False
                pos = pygame.mouse.get_pos()
                val = (','.join(map(str, pos)))
                valid = service.send(f'V{val}')
                if valid == "true" and elapsed >= 5:
                    service.send('INC_SCORE')

        # Test: Calculate countdown for game
        # if countdown > 0:
            # print(countdown)
            # count_timer = pygame.time.get_ticks()
            # if (count_timer - last_count) > 1000:
            #     x = random.randint(50, 650)
            #     y = random.randint(50, 650)
            #     win.blit(easteregg, (x, y))
            #     countdown -= 1
            #     last_count = count_timer

        pygame.display.update()

def show_menu():
    run = True
    win.blit(easterbg, (0, 0))
    draw_text("Easter Egg Game", font100, red, 70, 50)
    draw_text("Click to Play!", font60, red, 220, 400)
    pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Wait for other players
                connection_handler()
                # Begin game
                run = False

    main()

def make_coords(coords):
    return json.dumps({"mouse_coords":[(coords[0],coords[1])]})

# Handles drawing the eggs for all players
def egg_handler():
    # Request server for egg coordinates
    coords = service.send("EGG")
    coords_dic = json.loads(coords)

    # Draw eggs with server provided coordinates
    coords_lst = coords_dic["egg_coords"]
    for i, coord in enumerate(coords_lst):
        win.blit(easteregg, coord)

    # Request server for locked egg coordinates
    coords = service.send("LOCKED")
    coords_dic = json.loads(coords)
    
    # Draw eggs with server provided coordinates
    coords_lst = coords_dic["locked_coords"]
    for i, coord in enumerate(coords_lst):
        win.blit(easteregglocked, coord)

# Handles drawing coords and sending information to server to update other clients of position
def mouse_handler():
    # get player cursor coords
    pos = pygame.mouse.get_pos()
    
    # request other player's mice coordinates
    msg = service.send("MOUSE")
    coords = service.send(make_coords(pos))
    coords_dic = json.loads(coords)
    # draw every cursor except players own cursor
    coords_lst = coords_dic['mouse_coords']
    
    for i, coord in enumerate(coords_lst):
        if i != player_num:
            win.blit(cursors[i], coord)

    # draw player cursor on top of other players
    win.blit(cursors[player_num], pos)

def connection_handler():
    global player_num 
    win.blit(easterbg, (0, 0))
    draw_text("Waiting on other players...", font60, red, 100, 300)
    pygame.display.update()

    # Notifies server is ready, and server assigns player number
    player_num = int(service.send("READY"))

show_menu()

