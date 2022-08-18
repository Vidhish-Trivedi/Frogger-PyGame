import pygame as pg
from os import walk  # Built-in, used to go through folders (returns file name).

pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)

        # Adding images for animations.
        self.import_assets()
        self.frame_index = 0
        
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center=position)

        # Float based position
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2((0, 0))
        self.speed = 200

    def import_assets(self):
        img_path = "./graphics/player/right/"
        
        # List comprehension.
        self.animations = [pg.image.load(f"{img_path}{img}.png").convert_alpha() for img in range(4)]
        
        # For loop.
        # self.animations = []
        # for img in range(4):
        #         self.animations.append(pg.image.load(f"{img_path}{img}.png").convert_alpha())

    def move_player(self, deltaTime):
        if(self.direction.magnitude() != 0):
            self.direction = self.direction.normalize()
            self.animate_player(deltaTime)
            self.pos += self.direction*self.speed*deltaTime
            self.rect.center = (round(self.pos.x), round(self.pos.y))


    def input(self):
        keyboard_keys = pg.key.get_pressed()
        # The order of these if/elif/else statements will determine if we can move diagonally or not (Detect simultaneous key presses).
        if(keyboard_keys[pg.K_LEFT]):
            self.direction.x = -1
        elif(keyboard_keys[pg.K_RIGHT]):
            self.direction.x = 1
        else:
            self.direction.x = 0

        if(keyboard_keys[pg.K_UP]):
            self.direction.y = -1
        elif(keyboard_keys[pg.K_DOWN]):
            self.direction.y = 1
        else:
            self.direction.y = 0

    def animate_player(self, deltaTime):
        self.frame_index += 8*deltaTime  # For speed of animations.
        self.image = self.animations[int(self.frame_index)%(len(self.animations))]

    def update(self, deltaTime):
        self.input()
        self.move_player(deltaTime)

#################  ADJUST/NORMALIZE A VECTOR (OTHERWISE DIAGONAL SPEED WOULD BE SQRT(V1 + V2))  #####################
# Meaning length of vector should be 1.
#####################################################################################################################
