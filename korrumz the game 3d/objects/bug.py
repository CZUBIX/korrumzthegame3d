from ursina import *
from ursina.shaders import lit_with_shadows_shader

class Bug(Entity):
    def __init__(self, x, y, image_number):
        super().__init__()

        self.image_number = image_number

        self.model = "cube"
        self.texture = load_texture(f"./assets/bugs/bug{self.image_number}.png")
        
        self.position = (x, 2, y)
        self.scale = (75 / 10, 48 / 10, 75 / 10)

        self.shader = lit_with_shadows_shader