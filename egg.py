# Server will send this object to every client, and clients will show the images to game.
class Egg:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected = False

    def isSelected(self):
        return self.selected


