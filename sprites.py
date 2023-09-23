import pygame as pg
from settings import *
from tilemap import *
import math

vec = pg.math.Vector2

def hitbox_collide(sprite, other_sprite):
    if sprite.hit_rect.colliderect(other_sprite.rect):
        return True
    return False

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0 # start out pointing right is 0 degrees

    def get_keys(self):
        self.rot_speed = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc = vec(0, -PLAYER_ACC_WALK * 0.5).rotate(-self.rot)

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc = vec(0, PLAYER_ACC_WALK * 0.5).rotate(-self.rot)

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.acc = vec(PLAYER_ACC_WALK, 0).rotate(-self.rot)

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc = vec(-PLAYER_ACC_WALK / 2, 0).rotate(-self.rot)

        if keys[pg.K_LSHIFT] and (keys[pg.K_w] or keys[pg.K_UP]):
            self.acc = vec(PLAYER_ACC_SPRINT, 0).rotate(-self.rot)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, hitbox_collide)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, hitbox_collide)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def rotate(self):
        radius = 2 * TILESIZE
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - WIDTH / 2, mouse_y - HEIGHT / 2
        if math.hypot(rel_x, rel_y) > radius:
            self.rot = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pg.transform.rotate(self.game.player_img, int(self.rot))
            self.rect = self.image.get_rect()

    def limit_velocity(self, max_vel):
        min(-max_vel, max(self.vel.x, max_vel))
        if abs(self.vel.x) < 0.01:
            self.vel.x = 0

    def update(self):
        self.acc = vec(0, 0)
        self.get_keys()
        self.acc += self.vel * PLAYER_FRICTION  # apply friction
        self.vel += self.acc * self.game.dt     # add acceleration to velocity
        # self.limit_velocity(PLAYER_MAX_VEL)
        self.pos += self.vel * self.game.dt - (self.acc * 0.5) * (self.game.dt**2)  # calculate new position
        self.rotate()
        # self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        # self.image = pg.transform.rotate(self.game.player_img, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.hit_rect.center

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0
        
    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.floors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.floor_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
