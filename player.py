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
        self.hitbox = self.rect.inflate(0, -self.rect.height/2) # For collisions while keeping overlap.

    def collision(self, direction):
        # Using hitbox for collisions instead of rect.
        if(direction == "horizontal"):
            for sprite in self.collision_objects.sprites():
                if sprite.hitbox.colliderect(self.hitbox):  # There is a collision on either left or right side.
                    if(hasattr(sprite, 'name') and sprite.name == "car"):  # Collision with car.
                        pg.quit()
                        print("Game Over!")
                        sys.exit()
                    
                    if(self.direction.x > 0):  # Collision on left side. (moving rightwards).
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx  # To fix wobble on collision at high frame rates.
                        self.pos.x = self.hitbox.centerx  # To avoid ambiguity later in move_player() method.
                    
                    if(self.direction.x < 0):  # Collision on right side. (moving leftwards).
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
            
        else:  # direction == "vertical"
            for sprite in self.collision_objects.sprites():
                if sprite.hitbox.colliderect(self.hitbox):  # There is a collision on either top or bottom side.
                    if(hasattr(sprite, 'name') and sprite.name == "car"):  # Collision with car.
                        pg.quit()
                        print("Game Over!")
                        sys.exit()

                    if(self.direction.y > 0):  # Collision on top side. (moving downwards).
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery  # To fix wobble on collision at high frame rates.
                        self.pos.y = self.hitbox.centery  # To avoid ambiguity later in move_player() method.
                    
                    if(self.direction.y < 0):  # Collision on bottom side. (moving upwards).
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.hitbox.y = self.hitbox.centery

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

            # Seperating the horizontal and vertical movements, for collisions.
            # Horizontal movement.
            self.pos.x += self.direction.x*self.speed*deltaTime
            self.hitbox.centerx = round(self.pos.x)  # For collision.
            self.rect.centerx = self.hitbox.centerx  # For update.
            # Horizontal collisions.
            self.collision("horizontal")
            
            # Vertical movement.
            self.pos.y += self.direction.y*self.speed*deltaTime
            self.hitbox.centery = round(self.pos.y)  # For collision.
            self.rect.centery = self.hitbox.centery  # For update.
            # Vertical collisions.
            self.collision("vertical")
    
    # self.rect and self.hitbox maintain the same center. [IMPORTANT].

    def restrict(self):
        if(self.rect.left < 620):
            self.pos.x = 620 + self.rect.width/2
            self.hitbox.left = 620
            self.rect.left = 620

        if(self.rect.right > 2540):
            self.pos.x = 2540 - self.rect.width/2
            self.hitbox.right = 2540
            self.rect.right = 2540
        
        if(self.rect.bottom > 3480):
            self.pos.y = 3480 - self.rect.height/2
            self.rect.bottom = 3480
            self.hitbox.centery = self.rect.centery  # As hitbox is a bit shorter than the rect.

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
        self.animate_player(deltaTime)
        self.restrict()
