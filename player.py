import pygame as pg
from os import walk  # Built-in, used to go through folders (returns file name).

pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)

        # Adding images for animations.
        self.import_assets()
        self.frame_index = 0
        self.move_dir = 'right'
        
        self.image = self.animations['right'][self.frame_index]
        self.rect = self.image.get_rect(center=position)

        # Float based position
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2((0, 0))
        self.speed = 200

    def import_assets(self):
        # Better Import, using os.walk() method.
        main_path = "./graphics/player"
        self.animations = {}  # Dictionary:
        # (key, value) ==> key is direction (up, left, right, down) and value is list of pygame surfaces.
        for (index, folder) in enumerate(walk(main_path)):
            if(index == 0):
                for subfolder in folder[1]:
                    self.animations[subfolder] = []
            else:
                for file in folder[2]:
                    subfolder = folder[0].split("\\")[::-1][0]
                    img_path = main_path + "/" + subfolder + "/" + file
                    # print(img_path)
                    surf = pg.image.load(img_path).convert_alpha()
                    self.animations[subfolder].append(surf)

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
            self.move_dir = 'left'
        elif(keyboard_keys[pg.K_RIGHT]):
            self.direction.x = 1
            self.move_dir = 'right'
        else:
            self.direction.x = 0

        if(keyboard_keys[pg.K_UP]):
            self.direction.y = -1
            self.move_dir = 'up'
        elif(keyboard_keys[pg.K_DOWN]):
            self.direction.y = 1
            self.move_dir = 'down'
        else:
            self.direction.y = 0

    def animate_player(self, deltaTime):
        if(self.direction.magnitude() != 0):
            self.frame_index += 10*deltaTime  # For speed of animations.
            if(self.frame_index >= len(self.animations[self.move_dir])):
                self.frame_index = 0  # Loop around: 012301230123...
        
        else:
            self.frame_index = 0  # Standing position when not moving.

        self.image = self.animations[self.move_dir][int(self.frame_index)]

    def update(self, deltaTime):
        self.input()
        self.move_player(deltaTime)

#################  ADJUST/NORMALIZE A VECTOR (OTHERWISE DIAGONAL SPEED WOULD BE SQRT(V1 + V2))  #####################
# Meaning length of vector should be 1.
#####################################################################################################################
