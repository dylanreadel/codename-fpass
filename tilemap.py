import pygame as pg
from settings import *

def collide_hit_rect(one, two):
    # compare hit rect of player w/ rect of wall
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'r') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    # use a camera to draw the objects by an offset
    # the actual location of the objects are not moved
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # move camera for each sprite
        return entity.rect.move(self.camera.topleft) # returns new rectangle shifted by x, y amount
    
    def update(self, target):
        # update camera to follow the player at the middle of the screen
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        # x = min(0, x) # left
        # y = min(0, y) # top
        # x = max(-(self.width - WIDTH), x) # right
        # y = max(-(self.height - HEIGHT), y) # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)
