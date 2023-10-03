# Open World Survival Game (first pass)
# Credit to KidsCanCode on YouTube w/ Tile-based Game Tutorial

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
import spritesheet

# HUD functions
def draw_player_health(surf, x, y, percent_health):
    if percent_health < 0:
        percent_health = 0
    BAR_LENGTH = 250
    BAR_HEIGHT = 40
    fill = percent_health * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if percent_health > 0.6:
        col = GREEN
    elif percent_health > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_player_kills(surf, x, y, kills):
    pass

class Game:
    def __init__(self):
        # initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(250, 100) # 500ms delay, then 100ms interval for key repeat
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, "map")
        img_folder = path.join(game_folder, "img")
        self.map = TiledMap(path.join(map_folder, "Tiled1_TEST.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_img = pg.transform.scale(self.bullet_img, (10, 5))
        self.gun_muzzle_flashes = []
        for img in GUN_MUZZLE_FLASHES:
            self.gun_muzzle_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.gun_smoke = []
        for img in GUN_SMOKE:
            self.gun_smoke.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.mob_hit_effects = []
        for img in MOB_HIT_EFFECTS:
            self.mob_hit_effects.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.player_walk_effects = []
        for img in PLAYER_WALK_EFFECTS:
            self.player_walk_effects.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        ss = spritesheet.Spritesheet(path.join(img_folder, 'roguelikeitems.png'))
        for item in ITEM_IMAGES:
            ss_pos_x = ITEM_IMAGES[item][0] * SS_TILESIZE
            ss_pos_y = ITEM_IMAGES[item][1] * SS_TILESIZE
            scale_size = SS_TILESIZE * 2
            self.item_images[item] = pg.transform.scale(ss.image_at((ss_pos_x, ss_pos_y, SS_TILESIZE, SS_TILESIZE)),
                                                                    (scale_size, scale_size))
        # self.health_img = self.load_ss_image(health_ss_x, health_ss_y, ss)
        # self.health_img = pg.transform.scale(ss.image_at((176, 64, 16, 16)), (32, 32))

    # def load_ss_image(self, ss_loc_x, ss_loc_y, ss):
    #     pg.transform.scale(ss.image_at((ss_loc_x * SS_TILESIZE, ss_loc_y * SS_TILESIZE, SS_TILESIZE, SS_TILESIZE)), (SS_TILESIZE*2, SS_TILESIZE*2))

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.obstacles = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bullet_tracers = pg.sprite.Group()
        self.player_walk_effects_grp = pg.sprite.Group()
        self.items = pg.sprite.Group()

        # for row, tiles in enumerate(self.map.data):
        #     for column, tile in enumerate(tiles):
        #         if tile == "1":
        #             Wall(self, column, row)
        #         if tile == "P":
        #             self.player = Player(self, column, row)
        #         # if tile == ".":
        #         #     Floor(self, column, row)
        #         if tile == "M":
        #             Mob(self, column, row)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == "obstacle":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "mob":
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name in ITEMS:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

        self.run()

    def run(self):
        # run game loop
        # keep running at the right speed
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # game loop update
        self.all_sprites.update()
        self.camera.update(self.player)

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
            pos = hit.pos + MOB_HIT_OFFSET.rotate(-hit.rot)
            MobHitEffects(self, pos)

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

    def draw(self):
        # game loop draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(TAN)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for obstacle in self.obstacles:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(obstacle.rect), 1)
        
        # radius = 2 * TILESIZE
        # pg.draw.circle(self.screen, RED, (WIDTH / 2, HEIGHT / 2), radius, 2)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # after drawing everything, flip the display

        # draw HUD
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()

    def show_start_screen(self):
        # splash screen
        pass

    def show_gameover_screen(self):
        # game over or continue playing screen
        pass

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.show_gameover_screen()
