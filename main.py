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
all_sprites = AllSprites()  # For updating and drawing.
obstacle_sprites = pg.sprite.Group()  # Seperate group for checking collisions: (all_sprites - {my_player}).

# Create Instances.
player_start_pos = (2062, 3274)
my_player = Player(player_start_pos, all_sprites, obstacle_sprites)  # obstacle_sprites needs to be passed as an argument.
car_list = []

# Create timer(s).
car_timer = pg.event.custom_type()
pg.time.set_timer(car_timer, 80)

# Sprite setup for level objects.
for (file_name, pos_list) in st.SIMPLE_OBJECTS.items():
    surf = pg.image.load(f"./graphics/objects/simple/{file_name}.png").convert_alpha()
    for pos in pos_list:
        new_sprite_object = SimpleSprite(surface=surf, position=pos, groups=[all_sprites, obstacle_sprites])

for (file_name, pos_list) in st.LONG_OBJECTS.items():
    surf = pg.image.load(f"./graphics/objects/long/{file_name}.png").convert_alpha()
    for pos in pos_list:
        new_sprite_object = LongSprite(surface=surf, position=pos, groups=[all_sprites, obstacle_sprites])

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
                new_car = Car(car_pos, [all_sprites, obstacle_sprites])
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

##################################################################  COLLISIONS  ###################################################################
# So far, we just checked overlaps for collisions.
# Pygame can tell us if there is contact, we have to create our own collision logic.
# Updating elements before drawing is crucial, as it is during update that we will use collision logic.

# But, pygame only ever sees one frame at a time, so we don't have information about direction of approach.
# We first move in the horizontal direction and resolve horizontal collisions,
# then we move in the vertical direction and resolve vertical collisions.

# We can do two things:
# --> Direction: what we will do, easy to implement, but does not work when both objects are moving.  (for collisions of player with static objects).
    # So, one of the two colliding bodies should be stationary.

# --> Position: On every frame, we will store positions and compare them to positions in the next frame for both bodies, then check how they changed.
    # Works for 2 moving bodies also, but is more difficult.

# For collision of player with moving cars --> Game over scenario, so don't need proper collisions.

####################################################################################################################################################
