import json
import time

from client_game import ClientGame
from client_service import ClientService
from server import Server

# Color & Font
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DEFAULT_FONT = "comics"
ESCAPE = False
PLAYER_SCORES = ""

# Creates a JSON with client/server protocol including clients current mouse coordinates
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
    service.send("MOUSE")
    coords = service.send(make_coords(pos))
    service.updateCoordinates(coords)

    # draw every cursor except players own cursor
    coords_lst = service.extractCoordinates('mouse_coords')
    for i, coord in enumerate(coords_lst):
        if i != player_num:
            game.drawImage(cursors[i], coord)

    # draw player cursor on top of other players
    game.drawImage(cursors[player_num], pos)

# Handles displaying the current scores on each game loop
# flag determines the current state of the game
# if "PLAY" will print scores while game is still being played
# if "" will print scores on the results screen 
def score_handler(game, service, num_players, flag = ""):
    global PLAYER_SCORES
    if flag == "PLAY":
        # print player scores
        scores = service.send("SCORES")
        scores = scores[1:-1]
        PLAYER_SCORES = scores.split(', ')
        for i in range(0, num_players):
            game.drawText(f"Player {i + 1} Score: {PLAYER_SCORES[i]}", DEFAULT_FONT, 20, BLACK, i*200, 0)

    else:
        for i in range(0, num_players):
            game.drawText(f"Player {i + 1} Score: {PLAYER_SCORES[i]}", DEFAULT_FONT, 40, BLACK, 300, 200 + i*50)
            game.drawText("Press R to quit room", DEFAULT_FONT, 60, RED, 100, 600)

# Starts client service thread and requests to join server
# if flag set to "HOST" will spawn a server thread for players to join
# acting as a 'host' to the game
def connection_handler(game, flag = ""):
    easterbg = game.loadImage("img", "easterbg.jpg", (700, 700))
    game.drawImage(easterbg, (0, 0))
    game.drawText("Waiting on other players...", DEFAULT_FONT, 60, RED, 100, 300)
    
    if flag == "HOST":                    
        Server().start()
        game.drawText("Hosting!", DEFAULT_FONT, 60, RED, 100, 100)
        time.sleep(0.5)

    game.updateDisplay()

    service = ClientService()
    service.start()
    time.sleep(0.5)

    # Notifies server is ready, and server assigns player number
    player_num = int(service.send("READY"))
    return service, player_num

# Draws remaining time left in game
def time_handler(game, service):
    game_time = int(service.send("TIME"))
    game.drawText(f"Time: {game_time}", DEFAULT_FONT, 35, RED, 300, 20)

# Handles the scored points for the player
# If player successfully captures an egg will update the players current score
# and send it to the server
def point_handler(game, service, timer):
    elapsed = time.time() - timer
    position = game.getMousePosition()
    val = (','.join(map(str, position)))
    valid = service.send(f'V{val}:{elapsed}')
    if valid == "true":
        service.send('INC_SCORE')

# Setup to run game
# Sets up server if client decides to host
# Connects client to server IP/Port specified in client_service.py
def setup_client_host():
    game = ClientGame(700, 700, "Easter Egg Game")
    game.run()

    easterbg = game.loadImage("img", "easterbg.jpg", (700, 700))
    game.drawImage(easterbg, (0, 0))
    game.drawText("Easter Egg Game", DEFAULT_FONT, 100, RED, 70, 50)
    game.drawText("Press R to create room", DEFAULT_FONT, 60, RED, 100, 200)
    game.drawText("Press J to join room", DEFAULT_FONT, 60, RED, 100, 300)
    game.updateDisplay()

    service = None
    player_num = -1

    run = True
    while run:
        for event in game.getEvent():
            if event.type == game.QUIT:
                game.quit()
                run = False
            elif event.type == game.KEYDOWN:
                if event.key == game.R:
                    # Spawn(host) server thread + connect to that server
                    service, player_num = connection_handler(game, "HOST")
                    # Begin game
                    run = False
                elif event.key == game.J:
                    # Wait for other players
                    service, player_num = connection_handler(game)
                    # Begin game
                    run = False

    return game, service, player_num

# On every loop of the game it will be updated with the current state of the game:
# Server will supply egg locations, other clients cursor locations, current scores, and remaning time
# Client will update server with their own score and current cursor position
def client_loop(game, service, player_num):
    num_players = int(service.send("NUM"))
    print(num_players)
    cursors = game.loadCursors(num_players)

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
            score_handler(game, service, num_players, "PLAY")
            time_handler(game, service)
            
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
                    click_flag = False
                    point_handler(game, service, timer)

            game.updateDisplay()
        # use exception to end the game thread
        except:
            break

    # print Final Result
    run = True
    while run:
        game.fill(WHITE)
        score_handler(game, service, num_players)
        game.updateDisplay()

        for event in game.getEvent():
            if event.type == game.QUIT:
                game.quit()
                run = False 
            elif (event.type == game.KEYDOWN and event.key == game.R):
                game.quit()
                run = False

def main():
    game, service, player_num = setup_client_host()
    client_loop(game, service, player_num)
    service.join()

if __name__=='__main__':
    main()