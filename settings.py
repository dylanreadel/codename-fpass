# Game options and settings

import pygame as pg

RESOLUTIONS = {"HIGH": {"width": 2560, "height": 1440},
               "MEDIUM": {"width": 1920, "height": 1080},
               "LOW": {"width": 800, "height": 600}}

RESOLUTION = "MEDIUM"
WIDTH = RESOLUTIONS[RESOLUTION]["width"]
HEIGHT = RESOLUTIONS[RESOLUTION]["height"]
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
FPS = 144
TITLE = 'Codename: FPass (Open World Survival)'

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGRAY = (100, 100, 100)
DARKGREY = (40, 40, 40)
TAN = (179, 164, 123)

# Graphic settings
WALL_IMG = "tile_69.png"
FLOOR_IMG = "tile_07.png"

# Player settings
PLAYER_ACC_WALK = 400
PLAYER_ACC_SPRINT = 700
PLAYER_FRICTION = -2.5
PLAYER_MAX_VEL = 100
PLAYER_ROT_SPEED = 180 # degrees per second
PLAYER_IMG = 'survivor1_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 32, 32)

# Mob settings
MOB_IMG = "robot1_gun.png"

