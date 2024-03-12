from settings import *
from player import *
from dungeon import *

def display():
    screen.fill("#3d3d3d")

    for room in dungeon:
        for tile in room.tileGroup:
            tile.draw(player.xShift,player.yShift)

    for bullet in bulletGroup:
        bullet.draw(player.xShift,player.yShift)
    player.update()

    pygame.display.update()
    clock.tick(FPS)