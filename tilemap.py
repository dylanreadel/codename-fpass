import pygame as pg
import pytmx
from settings import *

def collide_hit_rect(one, two):
    # compare hit rect of sprite with another sprite's hit rect
    return one.hit_rect.colliderect(two.rect)

class Map:
    """read text map file"""
    def __init__(self, filename):
        self.data = []
        with open(filename, 'r') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    """read tiled map tmx file"""
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        tile_image = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tile_image(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))
                        
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

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
    
    def apply_rect(self, rect):
        # move camera for a rectangle
        return rect.move(self.camera.topleft)
    
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
