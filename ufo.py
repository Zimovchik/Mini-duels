import random
import pygame
import os
import sys

ball_spawn = False
WIDTH, HEIGHT = 800, 600
PLAYERONEKEY = pygame.K_s
PLAYERTWOKEY = pygame.K_k
SPEED = 0.5
all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
players = pygame.sprite.Group()
bg = pygame.sprite.Group()
score_board = pygame.sprite.Group()
BALL_RADIUS = 10
BULLET_SPEED = 1
spawns = [(45, HEIGHT // 2 - 64), (700, HEIGHT // 2 - 64)]
bulletspawns = [(150, HEIGHT // 2 - 10, 1), (550, HEIGHT // 2 - 10, -1)]
score = [0, 0]
player_color = [pygame.color.Color('blue'), pygame.color.Color('red')]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def reset():
    global all_sprites, balls, vertical_borders, horizontal_borders, players, bg, score_board
    global p1, p2, ball, red_score, blue_score
    all_sprites = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    players = pygame.sprite.Group()
    bg = pygame.sprite.Group()
    score_board = pygame.sprite.Group()
    p1 = Player(0, 1)
    p1.set_speed(0)
    p2 = Player(1, 1)
    p2.set_speed(0)
    ball = Bullet(*bulletspawns[random.randint(0, 1)])
    for i in star_generator(50):
        Star(*i)
    red_score = Score_board(0, 350, 10)
    blue_score = Score_board(0, 420, 10)


def star_generator(n):
    return [(random.randint(5, 20), random.randint(0, 800), random.randint(0, 600)) for i in range(n)]


def round_start():
    Bullet(*bulletspawns[random.randint(0, 1)])
    p1.set_position(*spawns[0])
    p1.set_speed(0)
    p1.set_direction(1)
    p2.set_position(*spawns[1])
    p2.set_speed(0)
    p2.set_direction(1)
    players.update()
    pygame.display.flip()
    for i in range(3, 0, -1):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font = pygame.font.SysFont('arial', 50)
        text = font.render(str(i), True, pygame.Color('yellow'))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        bg.draw(screen)
        all_sprites.draw(screen)
        players.draw(screen)
        balls.draw(screen)
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        pygame.time.delay(1000)


def win(screen_out, player):
    font = pygame.font.SysFont('arial', 50)
    text = font.render(f'player {player + 1} won', True, player_color[player])
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    screen_out.blit(text, (text_x, text_y))
    pygame.display.flip()


class Score_board(pygame.sprite.Sprite):
    def __init__(self, score, x, y):
        super().__init__(all_sprites)
        self.score = score
        self.image = load_image(f'ufo {score}.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (x, y)

    def set_score(self, n):
        self.image = load_image(f'ufo {n}.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Star(pygame.sprite.Sprite):
    def __init__(self, r, x, y):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("ufo_star.png"), (r, r))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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

    def set_position(self, x, y):
        self.pos = (x, y)

    def set_speed(self, v):
        self.vy = v

    def set_direction(self, dir):
        self.speed_direction = dir


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        super().__init__(balls, all_sprites)
        self.pos = (x, y)
        self.radius = BALL_RADIUS
        self.image = pygame.Surface((2 * self.radius,
                                     2 * self.radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.vx = BULLET_SPEED * dir
        self.vy = 0

    def update(self):
        self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.wall_collision()
        elif pygame.sprite.spritecollideany(self, vertical_borders):
            sprite = pygame.sprite.spritecollideany(self, vertical_borders)
            if self.rect.x <= 5:
                score[0] += 1
                blue_score.set_score(score[0])
            elif self.rect.x >= 595:
                score[1] += 1
                red_score.set_score(score[1])
            self.kill()
            if 3 not in score:
                round_start()
        self.velocity_limit()

    def ufo_collision(self, speed_direction):
        self.vx = -self.vx
        self.rect.move(-20, 0)
        self.rect.x = 10000
        self.vy = self.vy + speed_direction * SPEED

    def velocity_limit(self):
        if abs(int(self.vx)) > 2:
            self.vx = 2 * abs(self.vx) / self.vx
        if abs(int(self.vy)) > 2:
            self.vy = 2 * abs(self.vy) / self.vy

    def wall_collision(self):
        self.vy = -self.vy


p1 = Player(0, 1)
p1.set_speed(0)
p2 = Player(1, 1)
p2.set_speed(0)
ball = Bullet(*bulletspawns[random.randint(0, 1)])
for i in star_generator(50):
    Star(*i)
red_score = Score_board(0, 350, 10)
blue_score = Score_board(0, 420, 10)


def ufo_run(key_one, key_two):
    reset()
    pygame.init()
    pygame.display.set_caption('UFO')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    PLAYERONEKEY = key_one
    PLAYERTWOKEY = key_two

    # clock = pygame.time.Clock()
    top = Border(5, 5, WIDTH - 5, 5)
    bottom = Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    left = Border(5, 5, 5, HEIGHT - 5)
    right = Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
    running = True
    ending = False
    while running:
        screen.fill([19, 11, 77])
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == PLAYERONEKEY:
                    p1.change_direction()
                elif event.key == PLAYERTWOKEY:
                    p2.change_direction()
        if not ending:
            all_sprites.update()
            players.update()
            bg.draw(screen)
            all_sprites.draw(screen)
            players.draw(screen)
            balls.draw(screen)
            pygame.display.flip()
        if 3 in score and not ending:
            win(screen, score.index(3))
            ending = True
