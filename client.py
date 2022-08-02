import json
import time
import threading

from client_game import ClientGame
from client_service import ClientService
from server import Server

# Color & Font
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DEFAULT_FONT = "comics"
ESCAPE = False

def client_loop(game, service, player_num):
    score = ""
    num_players = service.send("NUM")
    print(num_players)
    num_players = int(num_players)
     # Player Cursors
    cursors = [None] * num_players
    for i in range(0, num_players):
        cursors[i] = game.loadImage("img", f"p{i+1}.png", (50, 50))

    game.fill(WHITE)
    game.setMouseVisible(False)

    click_flag = False
    timer = 0
    run = True
    while run:
        try:
            game.CLOCK.tick(60)
            game.fill(WHITE)
            egg_handler(game, service)
            mouse_handler(game, service, cursors, player_num)
            # print player scores
            scores = service.send("SCORES")
            scores = scores[1:-1]
            scores = scores.split(', ')
            PLAYER_SCORE = scores
            # print(scores)
            for i in range(0, num_players):
                game.drawText(f"Player {i+1} Score: {scores[i]}", DEFAULT_FONT, 20, BLACK, i*200, 0)

            for event in game.getEvent():
                if event.type == game.QUIT:
                    run = False
                    game.quit()

                elif event.type == game.MOUSEBUTTONDOWN:
                    position = game.getMousePosition()
                    # send pos to server
                    reply = service.send(','.join(map(str, position)))
                    # server will have database for positions of eggs
                    # if pos is in certain range (we have to choose), server will give a score to the player
                    print(reply)
                    if reply == 'clicked':
                        click_flag = True
                        timer = time.time()
                        
                elif click_flag and event.type == game.MOUSEBUTTONUP:
                    elapsed = time.time() - timer
                    click_flag = False
                    position = game.getMousePosition()
                    val = (','.join(map(str, position)))
                    valid = service.send(f'V{val}:{elapsed}')
                    if valid == "true":
                        service.send('INC_SCORE')
            game.updateDisplay()
        # use exception to end the game thread
        except:
            break

    # print Final Result
    run = True
    while run:
        game.fill(WHITE)
        for i in range(0, num_players):
            game.drawText(f"Player {i+1} Score: {scores[i]}", DEFAULT_FONT, 40, BLACK, 300, 200 + i*50)
            game.drawText("Press R to quit room", DEFAULT_FONT, 60, RED, 100, 600)
        game.updateDisplay()

        for event in game.getEvent():
            if event.type == game.QUIT:
                game.quit()
                run = False 
            elif (event.type == game.KEYDOWN and event.key == game.R):
                game.quit()
                run = False

def main():
    
    game = ClientGame(700, 700, "Easter Egg Game")
    game.run()
    
    service = None
    server = None

    easterbg = game.loadImage("img", "easterbg.jpg", (700, 700))
    game.drawImage(easterbg, (0, 0))
    game.drawText("Easter Egg Game", DEFAULT_FONT, 100, RED, 70, 50)
    game.drawText("Press R to create room", DEFAULT_FONT, 60, RED, 100, 200)
    game.drawText("Press J to join room", DEFAULT_FONT, 60, RED, 100, 300)
    game.updateDisplay()

    # initialized later via connection_handler
    player_num = -1

    run = True
    while run:
        for event in game.getEvent():
            if event.type == game.QUIT:
                game.quit()
                run = False

            elif event.type == game.KEYDOWN:
                if event.key == game.R:
                    Server().start()

                elif event.key == game.J:
                    service = ClientService()
                    service.start()
                    # Wait for other players
                    player_num = connection_handler(game, service)
                    # Begin game
                    run = False

    client_loop(game, service, player_num)
    service.join()

def make_coords(coords):
    return json.dumps({"mouse_coords":[(coords[0],coords[1])]})


# Handles drawing the eggs for all players
def egg_handler(game, service):
    easteregg = game.loadImage("img", "easteregg.png", (100, 100))
    easteregglocked = game.loadImage("img", "easteregglocked.png", (100, 100))

    # Request server for egg coordinates
    coords = service.send("EGG")
    service.updateCoordinates(coords)

    # Draw eggs with server provided coordinates
    coords_lst = service.extractCoordinates("egg_coords")
    for i, coord in enumerate(coords_lst):
        game.drawImage(easteregg, coord)

    # Request server for locked egg coordinates
    coords = service.send("LOCKED")
    service.updateCoordinates(coords)
    
    # Draw eggs with server provided coordinates
    coords_lst = service.extractCoordinates("locked_coords")
    for i, coord in enumerate(coords_lst):
        game.drawImage(easteregglocked, coord)


# Handles drawing coords and sending information to server to update other clients of position
def mouse_handler(game, service, cursors, player_num):
    # get player cursor coords
    pos = game.getMousePosition()
    
    # request other player's mice coordinates
    msg = service.send("MOUSE")
    coords = service.send(make_coords(pos))
    service.updateCoordinates(coords)

    # draw every cursor except players own cursor
    coords_lst = service.extractCoordinates('mouse_coords')
    for i, coord in enumerate(coords_lst):
        if i != player_num:
            game.drawImage(cursors[i], coord)

    # draw player cursor on top of other players
    game.drawImage(cursors[player_num], pos)


def connection_handler(game, service):
    easterbg = game.loadImage("img", "easterbg.jpg", (700, 700))
    game.drawImage(easterbg, (0, 0))
    game.drawText("Waiting on other players...", DEFAULT_FONT, 60, RED, 100, 300)
    game.updateDisplay()

    # Notifies server is ready, and server assigns player number
    player_num = int(service.send("READY"))
    return player_num


if __name__=='__main__':
    main()