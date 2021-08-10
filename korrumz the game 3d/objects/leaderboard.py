from ursina import *

class Leaderboard(Text):
    def __init__(self):
        super().__init__()

        self.visible = False
        self.origin = (0, 0)
        self.background = True