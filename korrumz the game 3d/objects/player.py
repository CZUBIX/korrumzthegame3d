from ursina import *
from ursina.shaders import lit_with_shadows_shader
from PIL import Image, ImageDraw

class Player(Entity):
    def __init__(self, username, x, y, pull_requests, image_number):
        super().__init__()

        self.username = username
        self.pull_requests = pull_requests
        self.image_number = image_number

        self.model = "cube"
        self.texture = load_texture(f"./assets/players/player{self.image_number}.png")
        
        self.position = (x, 5, y)
        self.scale = (75 / 10, 75 / 10, 75 / 10)

        img = Image.new("RGBA", (int(75 / 2), int(75 / 2)))
        draw = ImageDraw.Draw(img)
        draw.text((75 / 10 / 2, 75 / 10 / 2), self.username, (255, 255, 255))

        self.username_object = Entity(model="cube", texture=Texture(img), position=(x, 10, y), scale=(75 / 10, 75 / 10, 75 / 10))

        self.shader = lit_with_shadows_shader