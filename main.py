import pygame as pg
import sys
import settings as st
from player import Player
from car import Car

pg.init()

# This AllSprites will work as any other pygame group, but we can customize it.
class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pg.math.Vector2()  # To shift view.
        self.bg = pg.image.load('./graphics/main/map.png').convert()  # To be drawn below everything
        self.fg = pg.image.load('./graphics/main/overlay.png').convert_alpha()
    
    # Order of drawing (for perspective):
    # --> BG
    # --> Others (check for player in front/back of object (car)).**
    # --> FG

    def custom_draw(self):
        # Change offset vector.
        self.offset.x = my_player.rect.centerx - st.WINDOW_WIDTH/2
        self.offset.y = my_player.rect.centery - st.WINDOW_HEIGHT/2
        # Final offset should be negative, so that camera can move in opposite direction.

        display_surface.blit(self.bg, -self.offset)
        # We could also pass a surface as parameter,
        # but here, the required surface is in global scope.
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):  # ** Sorting by y-position, object with higher y-value is drawn over object with lower y-value.
            offset_pos = sprite.rect.center - self.offset
            display_surface.blit(sprite.image, offset_pos)

        display_surface.blit(self.fg, -self.offset)


# Create window.
display_surface = pg.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
pg.display.set_caption("Frogger")

# Create groups.
# all_sprites = pg.sprite.Group()
all_sprites = AllSprites()

# Create Instances.
my_player = Player((st.WINDOW_WIDTH/2, st.WINDOW_HEIGHT/2), all_sprites)
my_car = Car((1100, 200), all_sprites)

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

################################################################  CAMERA  ################################################################
# We cannot move the display_surface (window is fixed), however,
# we can move everything else in the opposite direction.
# Our game map has dimensions: (3200 x 3840), which is larger than our window.
# We would have a lot of moving rectangles, so we might not want to move all rects --> collisions will be difficult to manage.
# Instead of moving the rects, while drawing the sprites in the game loop, we will do so with an "offset". (group.draw())
# In this case, the original rect does not move, but is simply drawn with an offset, so managing collisions would not be more difficult.
# We can also customize the drawing order to create 3D-like effect with overlapping sprites. (player standing behind/ahead of some object).

###########################################################################################################################################
