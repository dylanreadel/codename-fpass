import pygame as pg
from settings import *
from tilemap import *
import math
import random as rand

vec = pg.math.Vector2

def hitbox_collide(sprite, other_sprite):
    if sprite.hit_rect.colliderect(other_sprite.rect):
        return True
    return False

def collide_with_group(sprite, group, dir):
    """check for collisions between a single sprite and group of sprites"""

    # check for collisions in x direction
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, hitbox_collide)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    # check for collisions in y direction
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, hitbox_collide)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0 # start out pointing right is 0 degrees
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.kills = 0
        self.elapsed_time = 0

    def player_effect(self):
        PlayerWalkEffects(self.game, self.pos)
        self.elapsed_time = 0

    def get_keys(self):
        self.rot_speed = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc = vec(0, -PLAYER_ACC_WALK * 0.5).rotate(-self.rot)     # LEFT

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc = vec(0, PLAYER_ACC_WALK * 0.5).rotate(-self.rot)      # RIGHT

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.acc = vec(PLAYER_ACC_WALK, 0).rotate(-self.rot)            # FORWARD
            self.elapsed_time += self.game.dt
            if self.elapsed_time > (self.game.dt * FPS) / 3:
                self.player_effect()

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc = vec(-PLAYER_ACC_WALK / 2, 0).rotate(-self.rot)       # BACKWARD

        if keys[pg.K_LSHIFT] and (keys[pg.K_w] or keys[pg.K_UP]):           # SPRINT
            self.acc = vec(PLAYER_ACC_SPRINT, 0).rotate(-self.rot)
        
        if keys[pg.K_SPACE]:                                                # SHOOT
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_FIRERATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + PLAYER_GUN_BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                self.vel = vec(BULLET_KICKBACK, 0).rotate(-self.rot)
                pos = self.pos + MUZZLE_FLASH_OFFSET.rotate(-self.rot)
                MuzzleFlash(self.game, pos)
                GunSmoke(self.game, pos)

    def rotate(self):
        # radius = 2 * TILESIZE
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - WIDTH / 2, mouse_y - HEIGHT / 2
        # if math.hypot(rel_x, rel_y) > radius:
        self.rot = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pg.transform.rotate(self.game.player_img, int(self.rot))
        self.rect = self.image.get_rect()

    def update(self):
        self.acc = vec(0, 0)
        self.get_keys()
        self.acc += self.vel * PLAYER_FRICTION  # apply friction
        self.vel += self.acc * self.game.dt     # add acceleration to velocity
        self.pos += self.vel * self.game.dt - (self.acc * 0.5) * (self.game.dt ** 2)  # calculate new position
        self.rotate()
        # self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        # self.image = pg.transform.rotate(self.game.player_img, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_group(self, self.game.obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_group(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy() # must use copy for multiple mobs
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = rand.choice(MOB_SPEED_RANGE)
        
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB_AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0.01).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * MOB_FRICTION
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + (self.acc * 0.5) * (self.game.dt ** 2)
        self.hit_rect.centerx = self.pos.x
        collide_with_group(self, self.game.obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_group(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.game.player.kills += 1
            self.kill()

    def draw_health(self):
        if self.health > int(MOB_HEALTH * (2/3)):
            col = GREEN
        elif self.health > int(MOB_HEALTH * (1/3)):
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

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

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer = OBSTACLE_LAYER
        self.groups = game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(self.game.bullet_img, self.game.player.rot)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        spread = rand.uniform(-BULLET_SPREAD, BULLET_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        BulletTracer(self.game, self.pos)
        if pg.sprite.spritecollideany(self, self.game.obstacles):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_DURATION:
            self.kill()

class BulletTracer(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.bullet_tracers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate((pg.Surface((2, 2), pg.SRCALPHA)), self.game.player.rot)
        self.image.fill(BULLET_TRACER)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > BULLET_TRACER_DURATION:
            self.kill()

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = 40
        self.image = pg.transform.rotate(pg.transform.scale(rand.choice(game.gun_muzzle_flashes), (size, size)),
                                         self.game.player.rot - 90)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > GUN_MUZZLE_FLASH_DURATION:
            self.kill()

class GunSmoke(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = 30
        self.image = pg.transform.rotate(pg.transform.scale(rand.choice(game.gun_smoke), (size, size)),
                                         self.game.player.rot - 90)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
        self.alpha = 255

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > GUN_SMOKE_DURATION:
            self.alpha = max(0, self.alpha - 0.25)
            self.image = self.image.copy()
            self.image.fill((255, 255, 255, self.alpha), special_flags=pg.BLEND_RGBA_MULT)
            if self.alpha <= 0:
                self.kill()

class MobHitEffects(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = 40
        self.image = pg.transform.rotate(pg.transform.scale(rand.choice(game.mob_hit_effects), (size, size)),
                                         self.game.player.rot - 90)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > MOB_HIT_DURATION:
            self.kill()

class PlayerWalkEffects(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = GROUND_EFFECTS_LAYER
        self.groups = game.all_sprites, game.player_walk_effects_grp
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = 40
        self.image = pg.transform.rotate(pg.transform.scale(rand.choice(game.player_walk_effects), (size, size)),
                                         self.game.player.rot - 90)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
        self.alpha = 255

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > PLAYER_WALK_DURATION:
            self.alpha = max(0, self.alpha - 1)
            self.image = self.image.copy()
            self.image.fill((255, 255, 255, self.alpha), special_flags=pg.BLEND_RGBA_MULT)
            if self.alpha <= 0:
                self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        # self.image = game.health_img
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
