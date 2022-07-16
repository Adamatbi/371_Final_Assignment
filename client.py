import random

import pygame
import os

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
easteregg = pygame.transform.scale(pygame.image.load(os.path.join("img", "easteregg.png")), (25, 25))

# Font
font100 = pygame.font.SysFont("comics", 100)
font60 = pygame.font.SysFont("comics", 60)

# Color
red = (255, 0, 0)
white = (255, 255, 255)

# Easy to calculate position (Temporary)
# test = pygame.transform.scale(pygame.image.load(os.path.join("img", "test.png")), (700, 700))

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    win.blit(img, (x, y))

def main():
    run = True
    win.fill(white)
    countdown = 10
    last_count = pygame.time.get_ticks()

    while run:
        clock.tick(60)
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
        if countdown > 0:
            print(countdown)
            count_timer = pygame.time.get_ticks()
            if (count_timer - last_count) > 1000:
                x = random.randint(50, 650)
                y = random.randint(50, 650)
                win.blit(easteregg, (x, y))
                countdown -= 1
                last_count = count_timer

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
                run = False
                # code for conect to server

    main()

show_menu()

