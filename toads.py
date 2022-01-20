import pygame
import os
import sys
import random

WIDTH, HEIGHT = 800, 600  # размеры экрана
GRAVITY = 1000  # гравитация
PLAYERONEKEY = pygame.K_a  # клавиши игроков
PLAYERTWOKEY = pygame.K_l
SPEED = 100  # скорость
JUMP_POWER = -300  # сила прыжка
LEVEL_WIDTH = 5000  # длина уровня
PLAYER_SIZE = 64  # размер игрока
K = 0.5  # коэффициент движения фона


def load_image(name, colorkey=None):  # загрузка изображения
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert(image)
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_map(filename):  # загрузка уровня из файла
    filename = 'data/maps/' + filename
    with open(filename, 'r') as mapFile:
        mapSettings, mapFile = tuple([line.strip() for line in mapFile])
        level_map = [line.strip().split('.') for line in mapFile.split(';')]
    for i in level_map[:-1]:
        print(i)
        if len(i):  # создание объектов
            if i[0] == 'p':
                Platform(int(i[1]), int(i[2]), int(i[3]), int(i[4]))
            elif i[0] == 'd':
                Death(int(i[1]), int(i[2]), int(i[3]), int(i[4]))
            else:
                print('unknohwn')
    global LEVEL_WIDTH, SPEEhD, GRAVITY, PLAYER_SIZE
    LEVEL_WIDTH, SPEED, GRAVITY, PLAYER_SIZE = tuple(
        map(lambda x: int(x), mapSettings.split(', ')))  # изменение настроек


def generate_map():  # создание уровня случайного
    for i in range(400, LEVEL_WIDTH, 250):
        j = random.randrange(HEIGHT // 3, HEIGHT - HEIGHT // 3)
        Death(i, 0, 50, j - PLAYER_SIZE // 2 * (5 - i // 750))
        Death(i, j + PLAYER_SIZE // 2 * (5 - i // 750), 50, HEIGHT - j - PLAYER_SIZE // 2 * (5 - i // 750))


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


def check_collision(first, second):  # проверка на столкновение у платформ и игрока
    y = (first.pos_y + first.rect.h) - second.rect.y
    y2 = first.pos_y - (second.rect.y + second.rect.h)
    if abs(y) > abs(y2):
        y = y2
    else:
        y = y
    x = first.pos_x + first.rect.w - second.rect.x
    if abs(y) > abs(x):
        first.pos_x -= x
        first.vx = 0
    else:
        first.pos_y -= y
        first.vy = 0
        first.gravity = 0


class Player(pygame.sprite.Sprite):  # класс игрока
    def __init__(self, color, player_number):
        super().__init__(char)
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 0, PLAYER_SIZE, PLAYER_SIZE), 0)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x = 0
        self.rect.y = self.pos_y = HEIGHT // 3 - self.rect.h // 2
        self.vx, self.vy = SPEED, 0
        self.gravity = GRAVITY
        self.is_alive = True
        self.color = pygame.Color(color)
        self.number = player_number
        self.frames = []
        self.cut_sheet(load_image('frog.png'), 8, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def update(self, ticks=0):
        if ticks:
            self.vy += self.gravity * ticks / 1000
            self.pos_x += self.vx * ticks / 1000
            self.pos_y += self.vy * ticks / 1000
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        if pygame.sprite.spritecollideany(self, platforms):
            for shprite in pygame.sprite.spritecollide(self, platforms, False):
                check_collision(self, shprite)
        else:
            self.gravity = GRAVITY
            self.vx = SPEED
        if self.rect.x + self.rect.w >= WIDTH:
            self.vx = 0
        if self.rect.x + self.rect.w < 0 or \
                pygame.sprite.spritecollideany(self, death) or self.rect.y >= HEIGHT or self.rect.y + self.rect.h < 0:
            # проверка на смерть
            self.kill()
            self.is_alive = False
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        sheet = pygame.transform.scale(sheet, (PLAYER_SIZE * columns, PLAYER_SIZE * rows))
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def jump(self):  # прыжок
        self.vy = JUMP_POWER
        self.update()

    def get_number(self):
        return self.number

    def get_color(self):
        return self.color


class Platform(pygame.sprite.Sprite):  # класс платформы
    def __init__(self, x, y, w, h):
        super().__init__(platforms, all_sprites)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("grey"), (0, 0, w, h), 0)
        self.pos_x, self.pos_y = x, y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, w, h)

    def update(self):
        self.rect.x, self.rect.y = self.pos_x, self.pos_y


class Death(pygame.sprite.Sprite):  # класс платформы, которая убивает
    def __init__(self, x, y, w, h):
        super().__init__(death, all_sprites)
        print(w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("white"), (0, 0, w, h), 0)
        self.pos_x, self.pos_y = x, y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, w, h)

    def update(self):
        self.rect.x, self.rect.y = self.pos_x, self.pos_y


class Camera:  # класс камеры
    def __init__(self):
        self.dx = 0
        self.length_left = LEVEL_WIDTH - WIDTH // 2  # длина пути камеры

    def update(self, ticks):  # вычисление сдвига
        if int(self.length_left) <= 0:
            self.dx = 0
        elif int(self.length_left) >= LEVEL_WIDTH - WIDTH:
            self.dx = 0
            self.length_left += -SPEED * ticks / 1000
        else:
            self.dx = -SPEED * ticks / 1000
            self.length_left += self.dx

    def apply(self, obj):  # сдвиг объекта
        obj.pos_x += self.dx
        obj.update()


class Background(pygame.sprite.Sprite):  # класс фона
    def __init__(self):
        super().__init__(background, all_sprites)
        self.image_1 = load_image('sky.png')
        j = LEVEL_WIDTH // self.image_1.get_rect().w + 1
        self.width = self.image_1.get_rect().w * j
        self.image = pygame.Surface((self.width, HEIGHT), pygame.SRCALPHA, 32)
        for i in range(j):
            print(i)
            self.image.blit(self.image_1, (self.image_1.get_rect().w * i, 0))
        self.rect = self.image.get_rect()
        self.pos_x, self.pos_y = 0, 0

    def update(self):  # движение фона
        self.rect.x = int(self.pos_x * K)
        self.rect.y = self.pos_y


pygame.init()
pygame.font.init()
pygame.display.set_caption('Toads')
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
death = pygame.sprite.Group()
char = pygame.sprite.Group()
background = pygame.sprite.Group()

back = Background()
# load_map('toadmap.txt')
generate_map()
players = []
player1 = Player('blue', 1)
players.append(player1)
player2 = Player('red', 2)
players.append(player2)
camera = Camera()

while running:  # игровой цикл
    players = list(filter(lambda g: g.rect.x + g.rect.w > 0, players))
    players = list(filter(lambda g: g.is_alive, players))
    if len(players) > 1:
        screen.fill((pygame.Color('black')))
        background.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == PLAYERONEKEY:
                    player1.jump()
                if event.key == PLAYERTWOKEY:
                    player2.jump()
        tick_passed = clock.tick()
        char.update(tick_passed)
        camera.update(tick_passed)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in char:
            camera.apply(sprite)
        all_sprites.draw(screen)
        char.draw(screen)
    elif len(players):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        win(screen, players[0])
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        tie(screen)
    pygame.display.flip()
