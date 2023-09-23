# Open World Survival Game (first pass)
# Credit to KidsCanCode on YouTube w/ Tile-based Game Tutorial

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

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
        self.map = Map(path.join(map_folder, "map2.txt"))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        # self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE)) # unnecessary here, just for notes
        self.floor_img = pg.image.load(path.join(img_folder, FLOOR_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.floors = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for column, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, column, row)
                if tile == "P":
                    self.player = Player(self, column, row)
                if tile == ".":
                    Floor(self, column, row)
                if tile == "M":
                    Mob(self, column, row)
        self.camera = Camera(self.map.width, self.map.height)

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

    # def draw_grid(self):
    #     for x in range(0, WIDTH, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    #     for y in range(0, HEIGHT, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def draw(self):
        # game loop draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(TAN)
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        # radius = 2 * TILESIZE
        # pg.draw.circle(self.screen, RED, (WIDTH / 2, HEIGHT / 2), radius, 2)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # after drawing everything, flip the display
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
