import threading
import pygame
import os

class ClientGame(threading.Thread):
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
    
    def __init__(self, width, height, caption):
        threading.Thread.__init__(self)
        self.daemon = True
        self.width = width
        self.height = height
        self.caption = caption

    def run(self):
        pygame.init()
        self.WINDOW = pygame.display.set_mode((self.width, self.height))
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption(self.caption)

    def fill(self, color):
        self.WINDOW.fill(color)

    def drawImage(self, image, position):
        self.WINDOW.blit(image, position)

    def loadImage(self, directory, file, size):
        return pygame.transform.scale(pygame.image.load(os.path.join(directory, file)), size)

    def drawText(self, text, font, size, color, x, y):
        fontSize = pygame.font.SysFont(font, size)
        image = fontSize.render(text, True, color)
        self.WINDOW.blit(image, (x, y))

    def updateDisplay(self):
        pygame.display.update()

    def getEvent(self):
        return pygame.event.get()

    def quit(self):
        pygame.quit()

    def setMouseVisible(self, isVisible):
        pygame.mouse.set_visible(isVisible)

    def getMousePosition(self):
        return pygame.mouse.get_pos()