import pygame
import os
import sys
from math import cos, sin, radians
from random import choice

WIDTH, HEIGHT = 800, 600
PLAYERONEKEY = pygame.K_a
PLAYERTWOKEY = pygame.K_l
SPEED = 0.25
all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
players = pygame.sprite.Group()
BALL_RADIUS = 10
BULLET_SPEED = 0.5
spawns = [(50, 32), (700, 400)]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Border(pygame.sprite.Sprite):  # window borders
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, p_number, speed_direction):
        super().__init__(players, all_sprites)
        self.pos = spawns[p_number]
        self.image = pygame.transform.flip(load_image(f"ufo player{p_number + 1}.png"), not p_number, False)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.vx = 0
        self.vy = SPEED
        self.speed_direction = speed_direction
        self.wall_colliding = False

    def change_direction(self):
        self.speed_direction = -self.speed_direction
        self.vy = self.speed_direction * SPEED

    def update(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.wall_collision(pygame.sprite.spritecollide(self, horizontal_borders, False)[0])
        elif pygame.sprite.spritecollideany(self, balls):
            sprite = pygame.sprite.spritecollideany(self, balls)
            sprite.ufo_collision(self.speed_direction)
        self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])

    def wall_collision(self, other):
        self.vy = 0
        if self.speed_direction == 1:
            self.pos = self.pos[0], other.rect.top - self.rect.h
        else:
            self.pos = self.pos[0], other.rect.bottom


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(balls, all_sprites)
        self.pos = (x, y)
        self.radius = BALL_RADIUS
        self.image = pygame.Surface((2 * self.radius,
                                     2 * self.radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.vx = BULLET_SPEED
        self.vy = 0

    def update(self):
        self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
        self.rect.x, self.rect.y = self.pos
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.wall_collision()

    def ufo_collision(self, speed_direction):
        self.vx = -self.vx
        self.rect.move(-20, 0)
        self.rect.x = 10000
        self.vy = self.vy + speed_direction * SPEED

    def wall_collision(self):
        self.vy = -self.vy


p1 = Player(0, 1)
p2 = Player(1, 1)
ball = Bullet(0, 300)


def ufo_run():
    pygame.init()
    pygame.display.set_caption('UFO')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    top = Border(5, 5, WIDTH - 5, 5)
    bottom = Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    left = Border(5, 5, 5, HEIGHT - 5)
    right = Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == PLAYERONEKEY:
                    p1.change_direction()
                elif event.key == PLAYERTWOKEY:
                    p2.change_direction()
        screen.fill((0, 0, 0))
        all_sprites.update()
        players.update()
        all_sprites.draw(screen)
        players.draw(screen)
        balls.draw(screen)
        pygame.display.flip()


ufo_run()
