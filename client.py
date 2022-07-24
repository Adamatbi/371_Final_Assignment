import random

import pygame
import os

from client_service import ClientService

# Initialize the pygame
pygame.init()

# Create the window and clock
width = 800
height = 800
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Caption
pygame.display.set_caption("Easter Egg Game")

# Backgroud and Image
easterbg = pygame.transform.scale(pygame.image.load(os.path.join("img", "easterbg.jpg")), (width, height))
easteregg = pygame.transform.scale(pygame.image.load(os.path.join("img", "easteregg.png")), (100, 100))

# Player Cursors
cursors = [pygame.transform.scale(pygame.image.load(os.path.join("img", "p1.png")), (50, 50)),
           pygame.transform.scale(pygame.image.load(os.path.join("img", "p2.png")), (50, 50)),
           pygame.transform.scale(pygame.image.load(os.path.join("img", "p3.png")), (50, 50)),
           pygame.transform.scale(pygame.image.load(os.path.join("img", "p4.png")), (50, 50))]

player_num = -1

# Font
font100 = pygame.font.SysFont("comics", 100)
font60 = pygame.font.SysFont("comics", 60)

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

def drawGrid():
    rect_size = 100
    for x in range(0, width, rect_size):
        for y in range(0, height, rect_size):
            rect = pygame.Rect(x, y, rect_size, rect_size)
            pygame.draw.rect(win, black, rect, 1)

def main():
    run = True
    win.fill(white)
    # countdown = 10
    last_count = pygame.time.get_ticks()
    pygame.mouse.set_visible(False)

    while run:
        clock.tick(60)
        win.fill(white)
        drawGrid()
        egg_handler()
        mouse_handler()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # send to pos to server
                # server will have database for positions of eggs
                # if pos is in certain range (we have to choose), server will give a score to the player
                # That egg will be locked

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
    draw_text("Easter Egg Game", font100, red, width / 8, height / 8)
    draw_text("Click to Play!", font60, red, width / 3, height / 2)
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


def read_coords(coords):
    coords = coords.split(',')
    return int(coords[0]), int(coords[1])


def make_coords(coords):
    return str(coords[0]) + "," + str(coords[1])


# Handles drawing the eggs for all players
def egg_handler():
    # Request server for egg coordinates
    coords = service.send("EGG")

    # Draw eggs with server provided coordinates
    coords_lst = coords.split('|')
    for i, coord in enumerate(coords_lst):
        egg_pos = read_coords(coord)
        win.blit(easteregg, egg_pos)


# Handles drawing coords and sending information to server to update other clients of position
def mouse_handler():
    # get player cursor coords
    pos = pygame.mouse.get_pos()

    # request other player's mice coordinates
    msg = service.send("MOUSE")
    coords = service.send(make_coords(pos))

    # draw every cursor except players own cursor
    coords_lst = coords.split('|')
    for i, coord in enumerate(coords_lst):
        other_pos = read_coords(coord)
        if i != player_num:
            win.blit(cursors[i], other_pos)

    # draw player cursor on top of other players
    win.blit(cursors[player_num], pos)


def connection_handler():
    global player_num
    win.blit(easterbg, (0, 0))
    draw_text("Waiting on other players...", font60, red, width / 6, height / 3)
    pygame.display.update()

    # Notifies server is ready, and server assigns player number
    player_num = int(service.send("READY"))

show_menu()