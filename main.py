import pygame as pg
import sys
import settings as st
from player import Player

pg.init()

# Create window.
display_surface = pg.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
pg.display.set_caption("Frogger")

# Create groups.
all_sprites = pg.sprite.Group()
# pl_grp = pg.sprite.GroupSingle()

# Create player.
my_player = Player((st.WINDOW_WIDTH/2, st.WINDOW_HEIGHT/2), all_sprites)


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
    all_sprites.draw(display_surface)

    # Keep window displayed.
    pg.display.update()
