import pygame as pg
from os import walk
import random

class Car(pg.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        # Selecting a random car from 3 choices.
        self.import_assets()
        self.image = random.choice(self.car_imgs)
        self.rect = self.image.get_rect(center=position)

        # Float based movement.
        self.pos = pg.math.Vector2(self.rect.center)

        # Car moves right.
        if(position[0] < 200):
            self.direction = pg.math.Vector2(1, 0)
        # Car moves left.
        elif(position[0] > 1080):
            self.image = pg.transform.flip(self.image, True, False)  # Flip image.
            self.direction = pg.math.Vector2(-1, 0)

        self.speed = 200
        self.name = "car"

    def import_assets(self):
        main_path = "./graphics/cars"
        self.car_imgs = []
        for (index, folders, files) in (walk(main_path)):
            for img in files:
                img_path = main_path + "/" + img
                surf = pg.image.load(img_path).convert_alpha()
                self.car_imgs.append(surf)

    def update(self, deltaTime):
        self.pos += self.direction*self.speed*deltaTime
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        # Remove cars outside 'map'.
        if(self.rect.x < - 200 or self.rect.x > 3400):  # 3200 is width of entire map (Later, we will see camera will move).
            self.kill()
