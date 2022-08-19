import pygame as pg

class SimpleSprite(pg.sprite.Sprite):
    def __init__(self, surface, position, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        
        self.hitbox = self.rect.inflate(0, -self.rect.height/2)  # For collisions while keeping overlap.

class LongSprite(pg.sprite.Sprite):
    def __init__(self, surface, position, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)

        self.hitbox = self.rect.inflate(-self.rect.width*(0.8), -self.rect.height/2)  # For collisions while keeping overlap.
        self.hitbox.bottom = self.rect.bottom - 10  # Setting hitbox a bit below the center of the sprite.
