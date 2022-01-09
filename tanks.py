import pygame
from math import cos, sin
import sys
import os

WIDTH, HEIGHT = 800, 600
PLAYERONEKEY = pygame.K_SPACE
PLAYERTWOKEY = pygame.K_UP
ANGLE_SPEED = 5
BULLET_SPEED = 30

all_sprites = pygame.sprite.Group()
char = pygame.sprite.Group()
bullets = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()


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


def win(screen_out, player):
    font = pygame.font.SysFont('arial', 50)
    text = font.render(f'player {player.number} won', True, player.color)
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    screen_out.blit(text, (text_x, text_y))


def tie(screen_out):
    font = pygame.font.SysFont('arial', 50)
    text = font.render(f'tie', True, pygame.Color('white'))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    screen_out.blit(text, (text_x, text_y))


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, color, player_number, player_image=None):
        super().__init__(char, all_sprites)
        self.pos = WIDTH // 2, HEIGHT // 2
        self.center = self.pos[0] + 32, self.pos[1] + 32
        self.color = pygame.Color(color)
        self.image = player_image
        self.angle = 0
        self.vx, self.vy = 0, 0
        self.is_alive = True
        self.number = player_number
        self.rect = self.image.get_rect()
        self.rot = 0
        self.rot_speed = 0
        self.last_update = pygame.time.get_ticks()
        self.image_orig = player_image

    def update(self, b):
        self.rotate()

    def shoot(self):
        # self.angle
        self.angle += 360
        print(f"angle: {self.angle}")

        Bullet(90, self.center)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.angle = self.rot - 90


class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, pos):
        # super().__init__(bullets, all_sprites)
        # print(pos, cos(angle), sin(angle))
        # self.image = bullet_image
        # self.rect = self.image.get_rect()
        # self.vx = BULLET_SPEED * cos(angle)
        # self.vy = BULLET_SPEED * sin(angle)
        # self.pos_x, self.pos_y = pos
        # self.pos_x -= 4
        # self.pos_y -= 4
        # self.mask = pygame.mask.from_surface(self.image)
        super().__init__(bullets, all_sprites)
        self.image = load_image("tanks bullet.png")
        self.rect = self.image.get_rect()

        self.vx, self.vy = BULLET_SPEED * cos(angle), BULLET_SPEED * sin(angle)

        self.x, self.y = pos
        self.x = self.x + 32 * cos(angle)
        self.y = self.y + 32 * sin(angle)

    def update(self, ticks=0):
        if ticks:
            self.x += self.vx * ticks / 1000
            self.y += self.vy * ticks / 1000
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.kill()
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.kill()


# if ticks:
#     self.pos_x += self.vx * ticks / 1000
#     self.pos_y += self.vy * ticks / 1000
# self.rect.x = int(self.pos_x)
# self.rect.y = int(self.pos_y)
# if self.rect.x + self.rect.w >= WIDTH or self.rect.y + self.rect.h >= HEIGHT:
#     self.kill()


bullet_image = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
pygame.draw.circle(bullet_image, pygame.Color("grey"), (8, 8), 8, 0)

pygame.init()
pygame.display.set_caption('Tanks')
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True
players = []
player1 = Player("red", "1", player_image=load_image("tank player1.png"))
players.append(player1)

Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

while running:
    screen.fill((pygame.Color('black')))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == PLAYERONEKEY:
                player1.shoot()
            # if event.key == PLAYERTWOKEY:
            #     player2.shoot()
        # if event.type == pygame.KEYUP:
        #     if event.key == PLAYERONEKEY:
        #         player1.shoot()
        # if event.key == PLAYERTWOKEY:
        #     player2.shoot()
    tick_passed = clock.tick()
    all_sprites.update(tick_passed)
    for i in players:
        screen.blit(i.image, (WIDTH // 2, HEIGHT // 2))
    for i in bullets:
        screen.blit(i.image, (i.rect.x, i.rect.y))
    pygame.display.flip()
