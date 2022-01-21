import os
import sys
from math import cos, sin, radians

import pygame

WIDTH, HEIGHT = 800, 600
PLAYERONEKEY = pygame.K_SPACE
PLAYERTWOKEY = pygame.K_UP
ANGLE_SPEED = 0.5
BULLET_SPEED = 1.5
BULLET_RADIUS = 10
TANK_SPEED = 0.3
players = [True, True]

all_sprites = pygame.sprite.Group()
boxes = pygame.sprite.Group()
p1bullets = pygame.sprite.Group()
p2bullets = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
tanks = pygame.sprite.Group()
win_window_sprites = pygame.sprite.Group()


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


def load_map(filename):
    with open(f"data/maps/{filename}", "r") as map:
        info = map.read()
        box_coordinates = [tuple(int(g) for g in i.split(',')) for i in info.split(';')]
    return box_coordinates


def set_boxes(coordinate_mass):
    for i in coordinate_mass:
        print(i)
        a = Box(*i, load_image("tank box.png"))


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
        elif pygame.sprite.spritecollideany(self, boxes):
            sprite = pygame.sprite.spritecollideany(self, boxes)
            self.kill()
            sprite.bullet_collision()

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
        self.rot_speed = ANGLE_SPEED
        self.last_update = pygame.time.get_ticks()
        self.image_orig = self.image.copy()
        self.player_alive = True
        self.orig_rot_speed = 0.25
        self.rotating = True
        self.player_number = player_number

    def update(self, ticks=0):
        if self.player_alive:
            if not self.rotating:
                self.collision()
                self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
                self.rect.x, self.rect.y = int(self.pos[0]), int(self.pos[1])
                # if pygame.sprite.spritecollideany(self, boxes):
                #     self.vx = 0
                #     self.vy = 0
                #     self.rotating = True

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

    def collision(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = 0
        else:
            self.vy = -TANK_SPEED * sin(radians(self.rot + 90))
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = 0
        else:
            self.vx = TANK_SPEED * cos(radians(self.rot + 90))

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


def win(screen_out, player):
    font = pygame.font.SysFont('arial', 50)
    text = font.render(f'player {player} won', True, "blue")
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 3 - text.get_height() // 2
    screen_out.blit(text, (text_x, text_y))


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


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, pic):
        super().__init__(boxes, all_sprites)
        self.bullet_counter = 0
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        Border(x, y, x + 64, y)
        Border(x, y + 64, x + 64, y + 64)
        Border(x, y, x, y + 64)
        Border(x + 64, y, x + 64, y + 64)

    def remove_box(self):
        self.rect.x = 10000
        self.rect.y = 10000
        self.kill()

    def bullet_collision(self):
        self.bullet_counter += 1
        if self.bullet_counter >= 10:
            self.remove_box()

    def set_bullet_count(self, n):
        self.bullet_counter = n

    def tank_collision(self):
        pass


class win_window(pygame.sprite.Sprite):
    def __init__(self, win_pic):
        super().__init__(win_window_sprites)
        self.image = win_pic
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


def tanks_run():
    p1 = Tank("red", 1, "tank player1.png", (720, 20))
    p2 = Tank("blue", 2, "tank player2.png", (80, 480))
    pygame.init()
    pygame.display.set_caption('Tanks')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    map_coords = load_map("tank_map.txt")
    set_boxes(map_coords)
    Border(5, 5, WIDTH - 5, 5)
    Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

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
                elif event.key == pygame.K_ESCAPE:
                    running = False
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
            win(screen, players.index(False) + 1)
        pygame.display.flip()