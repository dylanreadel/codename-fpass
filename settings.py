# Game options and settings

import pygame as pg
vec = pg.math.Vector2

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
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
LIGHTGRAY = (100, 100, 100)
DARKGREY = (40, 40, 40)
TAN = (179, 164, 123)

# Graphic settings
WALL_IMG = "tile_69.png"
FLOOR_IMG = "tile_07.png"

# Layer draw properties (higher number is drawn higher/last)
OBSTACLE_LAYER = 1
GROUND_EFFECTS_LAYER = 2
PLAYER_LAYER = 3
BULLET_LAYER = 4
MOB_LAYER = 3
EFFECTS_LAYER = 5
ITEMS_LAYER = 1

# Player settings
PLAYER_HEALTH = 100
PLAYER_ACC_WALK = 400
PLAYER_ACC_SPRINT = 700
PLAYER_FRICTION = -2.5
PLAYER_ROT_SPEED = 180 # degrees per second
PLAYER_IMG = 'survivor1_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 32, 32)
PLAYER_GUN_BARREL_OFFSET = vec(5, 10)
MUZZLE_FLASH_OFFSET = vec(35, 10)
PLAYER_WALK_EFFECTS = ["dirt_01.png", "dirt_02.png", "dirt_03.png"]
PLAYER_WALK_DURATION = 250

# Mob settings
MOB_IMG = "robot1_gun.png"
MOB_SPEED_RANGE = [200, 250, 300, 350, 400]
MOB_FRICTION = -2.5
MOB_HIT_RECT = pg.Rect(0, 0, 32, 32)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 40
MOB_AVOID_RADIUS = 50
MOB_HIT_EFFECTS = ["trace_01.png", "trace_02.png", "trace_03.png", "trace_04.png"]
MOB_HIT_DURATION = 100
MOB_HIT_OFFSET = vec(-20, 0)

# Bullet properties
BULLET_IMG = "weapon_gun.png"
BULLET_SPEED = 4000
BULLET_DURATION = 200
BULLET_FIRERATE = 300
BULLET_KICKBACK = -25
BULLET_SPREAD = 5
BULLET_DAMAGE = 40

# Gun properties
GUN_MUZZLE_FLASHES = ["muzzle_01.png", "muzzle_02.png", "muzzle_03.png",
                      "muzzle_04.png", "muzzle_05.png"]
GUN_SMOKE = ["smoke_01.png", "smoke_02.png", "smoke_03.png",
             "smoke_04.png", "smoke_05.png", "smoke_06.png",
             "smoke_07.png"]
GUN_MUZZLE_FLASH_DURATION = 40
GUN_SMOKE_DURATION = 500

BULLET_TRACER = (255, 255, 255, 100)
BULLET_TRACER_DURATION = 2000

# Spritesheet item locations
SS_TILESIZE = 16

health_ss_x, health_ss_y = 11, 4

# Item properties
ITEMS = ['health', 'sword']
ITEM_IMAGES = {'health': (11, 4), 'sword': (3, 7)}
