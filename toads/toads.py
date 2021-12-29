import pygame
import os
import sys

WIDTH, HEIGHT = 800, 600
GRAVITY = 700
PLAYERONEKEY = pygame.K_SPACE
PLAYERTWOKEY = pygame.K_UP
SPEED = 100
LEVEL_WIDTH = 1200


def load_image(name, colorkey=None):
    fullname = os.path.join('data/images', name)
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


def terminate():
    pygame.quit()
    sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__(char)
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 0, 64, 64), 0)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x = 0
        self.rect.y = self.pos_y = HEIGHT // 3 - self.rect.h // 2
        self.vx, self.vy = SPEED, 0
        self.gravity = GRAVITY

    def update(self, ticks=0):
        if ticks:
            self.vy += self.gravity * ticks / 1000
            self.pos_x += self.vx * ticks / 1000
            self.pos_y += self.vy * ticks / 1000
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        if pygame.sprite.spritecollideany(self, platforms):
            if self.vy >= 0:
                self.gravity = 0
            else:
                self.rect.y = self.pos_y = self.pos_y + 1
                self.gravity = GRAVITY
            self.vy = 0
        elif pygame.sprite.spritecollideany(self, walls):
            self.vx = 0
            self.gravity = GRAVITY
        else:
            self.vx = SPEED
            self.gravity = GRAVITY
        if self.rect.x + self.rect.w >= WIDTH:
            self.vx = 0
        if self.rect.x + self.rect.w < 0 or pygame.sprite.spritecollideany(self, death):
            self.kill()

    def jump(self):
        self.pos_y -= 1
        self.vy = -350
        self.update()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(walls, all_sprites)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("purple"), (0, 0, w, h), 0)
        self.pos_x, self.pos_y = x, y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, w, h)

    def update(self):
        self.rect.x, self.rect.y = self.pos_x, self.pos_y


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(platforms, all_sprites)
        self.image = pygame.Surface((w - 1, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("grey"), (0, 0, w - 1, h), 0)
        Wall(x, y, 5, h)
        self.pos_x, self.pos_y = x, y
        self.rect = pygame.Rect(self.pos_x + 1, self.pos_y, w - 1, h)

    def update(self):
        self.rect.x, self.rect.y = self.pos_x + 5, self.pos_y


class Death(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(death, all_sprites)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("white"), (0, 0, w, h), 0)
        self.pos_x, self.pos_y = x, y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, w, h)

    def update(self):
        self.rect.x, self.rect.y = self.pos_x, self.pos_y


class Camera:
    def __init__(self):
        self.dx = 0
        self.length_left = LEVEL_WIDTH - WIDTH // 2

    def update(self, ticks):
        if int(self.length_left) <= 0:
            self.dx = 0
        elif int(self.length_left) >= LEVEL_WIDTH - WIDTH:
            self.dx = 0
            self.length_left += -SPEED * ticks / 1000
        else:
            self.dx = -SPEED * ticks / 1000
            self.length_left += self.dx
        print(int(self.length_left))

    def apply(self, obj):
        obj.pos_x += self.dx
        obj.update()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Toads')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    death = pygame.sprite.Group()
    char = pygame.sprite.Group()

    players = []
    player1 = Player('blue')
    players.append(player1)
    player2 = Player('red')
    players.append(player2)
    Platform(10, 500, 700, 30)
    Platform(100, 300, 400, 210)
    Platform(900, 100, 400, 210)
    Platform(810, 590, 600, 30)
    Death(400, 100, 100, 100)
    camera = Camera()

    while running:
        screen.fill((pygame.Color('black')))
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
        players = list(filter(lambda g: g.rect.x + g.rect.w > 0, players))
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in char:
            camera.apply(sprite)
        all_sprites.draw(screen)
        char.draw(screen)
        pygame.display.flip()
