# Server controls this
class Game:
    def __init__(self, id):
        self.id = id
        self.ready = False
        self.score = [0, 0]
        self.wins = [0, 0]
        self.ties = 0

    def connected(self):
        return self.ready

    def winner(self):
        winner = -1
        if self.score[0] > self.score[1]:
            winner = 0
        if self.score[0] < self.score[1]:
            winner = 1

        return winner

    def resetGame(self):
        self.score = [0, 0]

