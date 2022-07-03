class Player():
    """ The player class is the person playing the game and is responsible for keeping track of
    the score of the game"""

    def __init__(self):
        self._score = 0

    def get_score(self):
        return str(self._score)

    def set_score(self, score):
        self._score += score