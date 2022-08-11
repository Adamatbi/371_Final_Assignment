import pygame
import os

# Front End part for client
class ClientGame():
    # Window and Clock
    WINDOW = None
    CLOCK = None

    # Event
    QUIT = pygame.QUIT
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
    MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
    KEYDOWN = pygame.KEYDOWN
    R = pygame.K_r
    J = pygame.K_j

    # Initialization
    def __init__(self, width, height, caption):
        self.width = width
        self.height = height
        self.caption = caption

    # Pygame start and display window
    def run(self):
        pygame.init()
        self.WINDOW = pygame.display.set_mode((self.width, self.height))
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption(self.caption)

    # Fill window with color
    def fill(self, color):
        self.WINDOW.fill(color)

    # Draw image to window
    def drawImage(self, image, position):
        self.WINDOW.blit(image, position)

    # Get image file from directory
    def loadImage(self, directory, file, size):
        return pygame.transform.scale(pygame.image.load(os.path.join(directory, file)), size)

    # Get cursor images of all players
    def loadCursors(self, num_players):
        cursors = []
        for i in range(1, num_players + 1):
            cursors.append(self.loadImage("img", f"p{i}.png", (50, 50)))

        return cursors

    # Display text to window
    def drawText(self, text, font, size, color, x, y):
        fontSize = pygame.font.SysFont(font, size)
        image = fontSize.render(text, True, color)
        self.WINDOW.blit(image, (x, y))

    # Refresh window for update
    def updateDisplay(self):
        pygame.display.update()

    # Get pygame event from players
    def getEvent(self):
        return pygame.event.get()

    # Quit pygame
    def quit(self):
        pygame.quit()

    # Set mouse visible or invisible
    def setMouseVisible(self, isVisible):
        pygame.mouse.set_visible(isVisible)

    # Get mouse position of players
    def getMousePosition(self):
        return pygame.mouse.get_pos()