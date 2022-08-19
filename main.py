import pygame as pg
import sys
import random
import settings as st
from player import Player
from car import Car
from sprite import SimpleSprite, LongSprite

pg.init()

# This AllSprites will work as any other pygame group, but we can customize it.
class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pg.math.Vector2()  # To shift view.
        self.bg = pg.image.load('./graphics/main/map.png').convert()
        self.fg = pg.image.load('./graphics/main/overlay.png').convert_alpha()

    def custom_draw(self):

        self.offset.x = my_player.rect.centerx - st.WINDOW_WIDTH/2
        self.offset.y = my_player.rect.centery - st.WINDOW_HEIGHT/2

        display_surface.blit(self.bg, -self.offset)
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.center - self.offset
            display_surface.blit(sprite.image, offset_pos)

        display_surface.blit(self.fg, -self.offset)

# Create window.
display_surface = pg.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
pg.display.set_caption("Frogger")

# Create groups.
all_sprites = AllSprites()  # Using our custom group class.

# Create Instances.
player_start_pos = (2062, 3274)
my_player = Player(player_start_pos, all_sprites)
car_list = []

# Create timer(s).
car_timer = pg.event.custom_type()
pg.time.set_timer(car_timer, 80)

# Sprite setup for level objects.
for (file_name, pos_list) in st.SIMPLE_OBJECTS.items():
    surf = pg.image.load(f"./graphics/objects/simple/{file_name}.png").convert_alpha()
    for pos in pos_list:
        new_sprite_object = SimpleSprite(surface=surf, position=pos, groups=all_sprites)

for (file_name, pos_list) in st.LONG_OBJECTS.items():
    surf = pg.image.load(f"./graphics/objects/long/{file_name}.png").convert_alpha()
    for pos in pos_list:
        new_sprite_object = LongSprite(surface=surf, position=pos, groups=all_sprites)

# Create clock to get delta time later.
clk = pg.time.Clock()

# Game loop.
while(True):
    # Event loop.
    for event in pg.event.get():
        if(event.type == pg.QUIT):
            pg.quit()
            print("Game Closed!")
            sys.exit()
    
        if(event.type == car_timer):
            # Logic to spawn cars so that they do not overlap (spawn at same location too quickly).
            car_pos = random.choice(st.CAR_START_POSITIONS)
            if(car_pos not in car_list):
                car_list.append(car_pos)
                # Can also do (random_x, random_y + random_y_offset) for more realistic car motion, like,
                # car_list.append((car_pos[0], car_pos[1] + random.randint(-8, 8))) # and then later remove this. 
                new_car = Car(car_pos, all_sprites)
            if(len(car_list) > 5):
                car_list.remove(car_list[0])

    # Delta time.
    dt = clk.tick(120)/1000

    # Draw background.
    display_surface.fill("black")

    # Update.
    all_sprites.update(dt)

    # Draw.
    # all_sprites.draw(display_surface)
    all_sprites.custom_draw()

    # Keep window displayed.
    pg.display.update()
