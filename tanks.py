import os
import sys
from math import cos, sin, radians

import pygame

WIDTH, HEIGHT = 800, 600
PLAYERONEKEY = pygame.K_SPACE
PLAYERTWOKEY = pygame.K_UP
ANGLE_SPEED = 5
BULLET_SPEED = 1.5
BULLET_RADIUS = 10
TANK_SPEED = 0.2
all_sprites = pygame.sprite.Group()
char = pygame.sprite.Group()
p1bullets = pygame.sprite.Group()
p2bullets = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
tanks = pygame.sprite.Group()

players = [True, True]


def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, angle, pn):
        if pn == 1:
            super().__init__(p1bullets)
        else:
            super().__init__(p2bullets)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("grey"),
                           (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.vx = BULLET_SPEED * cos(radians(angle + 90))
        self.vy = -BULLET_SPEED * sin(radians(angle + 90))
        self.pos = x, y
        self.player_number = pn

    def update(self):
        self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
        self.rect.x, self.rect.y = self.pos
        if pygame.sprite.spritecollideany(self, vertical_borders) or pygame.sprite.spritecollideany(self,
                                                                                                    horizontal_borders):
            self.kill()
        if pygame.sprite.spritecollideany(self, tanks):
            sprite = pygame.sprite.spritecollideany(self, tanks)
            if sprite.get_player_number() != self.player_number:
                sprite.kill()
                sprite.death()
                self.kill()

    def get_player_number(self):
        return self.player_number


class Tank(pygame.sprite.Sprite):
    def __init__(self, color, player_number, im_name, pos):
        super().__init__(all_sprites, tanks)
        self.color = color
        self.number = player_number
        self.image = load_image(im_name)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vx, self.vy = 0, 0
        self.rot = 0
        self.rot_speed = 0.125
        self.last_update = pygame.time.get_ticks()
        self.image_orig = self.image.copy()
        self.player_alive = True
        self.orig_rot_speed = 0.25
        self.rotating = True
        self.player_number = player_number

    def update(self, ticks=0):
        if self.player_alive:
            if not self.rotating:
                self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
                self.rect.x, self.rect.y = int(self.pos[0]), int(self.pos[1])
            if not self.player_alive:
                return
            if ticks and self.rotating:
                self.rotate(ticks)

    def rotate(self, ticks):
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.rot)
        self.rot += self.rot_speed
        self.rot %= 360

    def shoot(self):
        if self.player_alive:
            Bullet(10, *self.rect.center, self.rot, self.player_number)
            self.vx, self.vy = TANK_SPEED * cos(radians(self.rot + 90)), -TANK_SPEED * sin(radians(self.rot + 90))
            self.rotating = False

    def rotate_change(self):
        self.rotating = True
        self.rot_speed = -self.rot_speed
        self.vx, self.vy = 0, 0

    def get_rot(self):
        return self.rot

    def get_rot_speed(self):
        return self.rot_speed

    def get_pos(self):
        return self.pos

    def get_rect(self):
        return self.rect

    def get_player_number(self):
        return self.player_number

    def get_tank_info(self):
        return (
            self.get_pos(),
            self.get_rot_speed(),
            self.get_rect(),
            self.get_player_number()
        )

    def death(self):
        self.player_alive = False
        global players
        players[self.player_number - 1] = self.player_alive


p1 = Tank("red", 1, "tank player1.png", (100, 100))
p2 = Tank("blue", 2, "tank player2.png", (200, 200))
pygame.init()
pygame.display.set_caption('Tanks')
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((50, 255, 139))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == PLAYERONEKEY:
                p1.shoot()
            elif event.key == PLAYERTWOKEY:
                p2.shoot()
        elif event.type == pygame.KEYUP:
            if event.key == PLAYERONEKEY:
                p1.rotate_change()
            elif event.key == PLAYERTWOKEY:
                p2.rotate_change()
    tick_passed = clock.tick()
    p1.update(tick_passed)
    all_sprites.draw(screen)
    all_sprites.update(tick_passed)
    p1bullets.draw(screen)
    p2bullets.draw(screen)
    p1bullets.update()
    p2bullets.update()
    if not all(players):
        print(f"Выиграл игрок {players.index(False) + 1}")
    pygame.display.flip()
