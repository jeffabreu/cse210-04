from game.casting.actor import Actor

class Gem(Actor):
    """ The gem keeps track of the points assigned to an individual gem, each time a gem is caught 
    it becomes more valuable"""
    
    def __init__(self):
        super().__init__()
        self._score = 1

    def increase_score(self):
        self._score += 1

    def decrease_score(self):
        self._score += 1

    def get_score(self):
        return self._score

    def set_score(self, score):
        self._score = score