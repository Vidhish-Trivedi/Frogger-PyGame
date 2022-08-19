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
player_won = False  # To check if player won.

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

# Font.
font1 = pg.font.Font(None, 50)  # Use Default font of pygame.
txt_surf = font1.render("You Win!!!", True, "red", "yellow")
txt_rect = txt_surf.get_rect(center=(st.WINDOW_WIDTH/2, st.WINDOW_HEIGHT/2))


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
    if(player_won):
        display_surface.blit(txt_surf, txt_rect)

    # Update.
    if(my_player.pos.y > 1180):
        all_sprites.update(dt)
        
        # Draw.
        all_sprites.custom_draw()

    else:
        player_won = True

    # Keep window displayed.
    pg.display.update()

#######################################  TO REGAIN OVERLAP WHILE KEEPING COLLISION LOGIC  ##############################
# Every sprite will have 2 rects, one for position and another (smaller the the one for position) for collisions.
########################################################################################################################
