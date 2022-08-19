import pygame as pg
import sys
from os import walk  # Built-in, used to go through folders (returns file name).

class Player(pg.sprite.Sprite):
    def __init__(self, position, groups, coll_grp):
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

        # For collisions.
        self.collision_objects = coll_grp

    def collision(self, direction):
        # pg.sprite.spritecollide(self, self.collision_objects, True)
    
        # For more control for developer.
        # for sprite in self.collision_objects.sprites():
        #     if(sprite.rect.colliderect(self.rect)):  # Check for simple rect collision
        #         # sprite.kill()

        if(direction == "horizontal"):
            for sprite in self.collision_objects.sprites():
                if sprite.rect.colliderect(self.rect):  # There is a collision on either left or right side.
                    if(hasattr(sprite, 'name') and sprite.name == "car"):  # Collision with car.
                        pg.quit()
                        print("Game Over!")
                        sys.exit()
                    
                    elif(self.direction.x > 0):  # Collision on left side. (moving rightwards).
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.centerx  # To avoid ambiguity later in move_player() method.
                    
                    elif(self.direction.x < 0):  # Collision on right side. (moving leftwards).
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.centerx
            
        else:  # direction == "vertical"
            for sprite in self.collision_objects.sprites():
                if sprite.rect.colliderect(self.rect):  # There is a collision on either top or bottom side.
                    if(hasattr(sprite, 'name') and sprite.name == "car"):  # Collision with car.
                        pg.quit()
                        print("Game Over!")
                        sys.exit()

                    elif(self.direction.y > 0):  # Collision on top side. (moving downwards).
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.centery  # To avoid ambiguity later in move_player() method.
                    
                    elif(self.direction.y < 0):  # Collision on bottom side. (moving upwards).
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.centery

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
            # self.animate_player(deltaTime)  #######  Was a bug  #######

            # self.pos += self.direction*self.speed*deltaTime
            # self.rect.center = (round(self.pos.x), round(self.pos.y))

            # Seperating the horizontal and vertical movements, for collisions.
            # Horizontal movement.
            self.pos.x += self.direction.x*self.speed*deltaTime
            self.rect.centerx = round(self.pos.x)
            # Horizontal collisions.
            self.collision("horizontal")
            
            # Vertical movement.
            self.pos.y += self.direction.y*self.speed*deltaTime
            self.rect.centery = round(self.pos.y)
            # Vertical collisions.
            self.collision("vertical")



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
        self.animate_player(deltaTime)  # calling this method here fixes standing position bug.
