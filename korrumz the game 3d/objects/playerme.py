from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class PlayerMe(FirstPersonController):
    def __init__(self, username, x, y, image_number):
        super().__init__()

        self.username = username
        self.pull_requests = 0
        self.image_number = image_number

        self.speed = 500
        self.position = (x, 0, y)
        
    def input(self, key):
        pass