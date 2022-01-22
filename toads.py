import pygame
from pygame import transform as tr
import os
import sys
import random

WIDTH, HEIGHT = 800, 600  # размеры экрана
GRAVITY = 1000  # гравитация
PLAYERONEKEY = pygame.K_a  # клавиши игроков
PLAYERTWOKEY = pygame.K_l
SPEED = 100  # скорость
JUMP_POWER = 300  # сила прыжка
LEVEL_WIDTH = 5000  # длина уровня
PLAYER_SIZE = 96  # размер игрока
GRAVITY_DIRECTION = 1  # направление гравитации
K = 0.5  # коэффициент движения фона


def reset():
    global all_sprites, platforms, death, char, background, inversions, inversions, running
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    death = pygame.sprite.Group()
    char = pygame.sprite.Group()
    background = pygame.sprite.Group()
    inversions = pygame.sprite.Group()
    running = True


reset()


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
    global LEVEL_WIDTH, SPEED, GRAVITY, PLAYER_SIZE
    LEVEL_WIDTH, SPEED, GRAVITY, PLAYER_SIZE = tuple(
        map(lambda x: int(x), mapSettings.split(', ')))  # изменение настроек


def generate_map():  # создание уровня случайного
    invers_dir = 0
    for i in range(400, LEVEL_WIDTH, 250):
        j = random.randrange(int(HEIGHT // 2.5), int(HEIGHT - HEIGHT / 2.5))
        if random.randint(0, 1):
            Inversion(i, j - 32, 64, 64, invers_dir)
            invers_dir = (invers_dir + 1) % 2
        Death(i, 0, 64, j - PLAYER_SIZE // 2 * (5 - i // 750), True)
        Death(i, j + PLAYER_SIZE // 2 * (5 - i // 750), 64, HEIGHT - j - PLAYER_SIZE // 2 * (5 - i // 750))


def win(screen_out, player):
    font = pygame.font.SysFont('arial', 50)
    text = font.render(f'player {player.get_number()} won', True, player.get_color())
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    screen_out.blit(text, (text_x, text_y))
    pygame.display.flip()
    ending()


def tie(screen_out):
    font = pygame.font.SysFont('arial', 50)
    text = font.render(f'tie', True, pygame.Color('white'))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    screen_out.blit(text, (text_x, text_y))
    pygame.display.flip()
    ending()


def ending():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False


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

        self.frames = {}
        self.cut_sheet(load_image('toad_states.png'), 4)
        self.cur_frame = 0
        self.image = self.frames['still']

        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x = 0
        self.rect.y = self.pos_y = HEIGHT // 3 - self.rect.h // 2

        self.vx, self.vy = SPEED, 0
        self.gravity_direction = GRAVITY_DIRECTION
        self.gravity = GRAVITY * self.gravity_direction

        self.is_alive = True
        self.is_flipped = False
        self.color = pygame.Color(color)
        self.number = player_number
        self.does_collide = 0

    def update(self, ticks=0):
        if ticks:
            self.vy += self.gravity * ticks / 1000
            self.pos_x += self.vx * ticks / 1000
            self.pos_y += self.vy * ticks / 1000
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.check_cur_frame()
        if pygame.sprite.spritecollideany(self, platforms):
            for shprite in pygame.sprite.spritecollide(self, platforms, False):
                check_collision(self, shprite)
        else:
            self.gravity = GRAVITY * self.gravity_direction
            self.vx = SPEED
        if pygame.sprite.spritecollideany(self, inversions):
            if self.does_collide:
                pass
            else:
                self.gravity_direction *= -1
                self.does_collide = 1
                if self.is_flipped:
                    self.is_flipped = False
                else:
                    self.is_flipped = True
        else:
            self.does_collide = 0
            self.gravity = GRAVITY * self.gravity_direction
            self.vx = SPEED
        if self.rect.x + self.rect.w >= WIDTH:
            self.vx = 0
        if self.rect.x + self.rect.w < 0 or \
                pygame.sprite.spritecollideany(self,
                                               death) or self.rect.y >= HEIGHT or self.rect.y + self.rect.h < 0:
            # проверка на смерть
            self.is_alive = False
            self.image = pygame.transform.flip(self.frames['dead'], False, self.is_flipped)

    def check_cur_frame(self):
        if int(abs(self.vy)) <= 10:
            self.image = pygame.transform.flip(self.frames['still'], False, self.is_flipped)
        elif int(self.vy * self.gravity_direction) > 0:
            self.image = pygame.transform.flip(self.frames['down'], False, self.is_flipped)
        elif int(self.vy * self.gravity_direction) < 0:
            self.image = pygame.transform.flip(self.frames['up'], False, self.is_flipped)

    def cut_sheet(self, sheet, columns):
        sheet = tr.scale(sheet, (PLAYER_SIZE * columns, PLAYER_SIZE))
        states = ['dead', 'down', 'up', 'still']
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height())
        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            self.frames[states[i]] = sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size))

    def jump(self):  # прыжок
        self.vy = JUMP_POWER * -self.gravity_direction

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
    def __init__(self, x, y, w, h, flipped=False):
        super().__init__(death, all_sprites)
        print('wh', w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.rect = pygame.rect.Rect(x, y, w, h)
        image = load_image('death_platform.png').subsurface(pygame.rect.Rect(0, 0, w, h))
        self.image = tr.flip(image, False, flipped)
        self.pos_x, self.pos_y = x, y

    def update(self):
        self.rect.x, self.rect.y = self.pos_x, self.pos_y


class Inversion(pygame.sprite.Sprite):  # класс смена гравитации
    def __init__(self, x, y, w, h, direction):
        super().__init__(inversions, all_sprites)
        self.variants = []
        self.cut_sheet(load_image('inverses.png'), 2)
        self.image = self.variants[direction]
        self.pos_x, self.pos_y = x, y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, w, h)

    def update(self):
        self.rect.x, self.rect.y = self.pos_x, self.pos_y

    def cut_sheet(self, sheet, columns):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height())
        for i in range(columns):
            frame_location = (64 * i, 0)
            self.variants.append(tr.scale(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)), (self.rect.w, self.rect.h)))

    def get_cords(self):
        return self.rect.x, self.rect.y


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


def toads_run(key_one, key_two):
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Toads')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    global running
    PLAYERONEKEY = key_one
    PLAYERTWOKEY = key_two

    Background()
    # load_map('toadmap.txt')
    generate_map()
    player1 = Player('blue', 1)
    player2 = Player('red', 2)
    players = [player1, player2]
    camera = Camera()

    while running:  # игровой цикл
        screen.fill((pygame.Color('black')))
        background.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == PLAYERONEKEY:
                    player1.jump()
                if event.key == PLAYERTWOKEY:
                    player2.jump()
        tick_passed = clock.tick(60)
        char.update(tick_passed)

        camera.update(tick_passed)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in char:
            camera.apply(sprite)
        all_sprites.draw(screen)
        char.draw(screen)
        if len(list(filter(lambda g: g.is_alive, players))) == 1:
            win(screen, list(filter(lambda g: g.is_alive, players))[0])
        elif len(list(filter(lambda g: g.is_alive, players))) == 0:
            tie(screen)
        pygame.display.flip()
    reset()



