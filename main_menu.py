import os
import sys
import pygame

from tanks import tanks_run
from toads import toads_run
from ufo import ufo_run
from chickens import chickens_run

from race import race_run

pygame.init()
pygame.font.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
# sprite groups

all_sprites = pygame.sprite.Group()
games = pygame.sprite.Group()
setting_btns = pygame.sprite.Group()
pygame.display.set_caption('Menu')
# window control vars
running = True
setting_open = False
volume_on = False
button_registration = 0
player_number = 0
new_btn = None
PLAYERONEKEY = pygame.K_a
PLAYERTWOKEY = pygame.K_l
keys = {pygame.K_a: 'a',
        pygame.K_b: 'b',
        pygame.K_c: 'c',
        pygame.K_d: 'd',
        pygame.K_e: 'e',
        pygame.K_f: 'f',
        pygame.K_g: 'g',
        pygame.K_h: 'h',
        pygame.K_i: 'i',
        pygame.K_j: 'j',
        pygame.K_k: 'k',
        pygame.K_l: 'l',
        pygame.K_m: 'm',
        pygame.K_n: 'o',
        pygame.K_p: 'p',
        pygame.K_q: 'q',
        pygame.K_r: 'r',
        pygame.K_s: 's',
        pygame.K_t: 't',
        pygame.K_u: 'u',
        pygame.K_v: 'v',
        pygame.K_w: 'w',
        pygame.K_x: 'x',
        pygame.K_y: 'y',
        pygame.K_z: 'z'}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button(pygame.sprite.Sprite):
    def __init__(self, group, main, image):
        super().__init__(group)
        main.add(self)
        self.image = image
        self.rect = self.image.get_rect()

    def press(self):
        pass

    def remove(self):
        self.rect.x, self.rect.y = 2000, 2000

    def im_change(self, im):
        self.image = im


# This funcs are creating only to paste them into button classes, so they are with no any specific title
def a():  # chicken btn func
    print('chichken')
    chickens_run(PLAYERONEKEY, PLAYERTWOKEY)
    pygame.display.set_caption("Menu")


def b():  # tanks btn func
    print('tanks')
    tanks_run(PLAYERONEKEY, PLAYERTWOKEY)
    pygame.display.set_caption("Menu")


def c():  # toads btn func
    print("toads")
    toads_run(PLAYERONEKEY, PLAYERTWOKEY)
    pygame.display.set_caption("Menu")


def d():
    print('ufos')
    ufo_run(PLAYERONEKEY, PLAYERTWOKEY)
    pygame.display.set_caption("Menu")


def e():
    print("race")
    race_run(PLAYERONEKEY, PLAYERTWOKEY)
    pygame.display.set_caption("Menu")


def sett():
    global setting_open
    setting_open = not setting_open


def btn_change(player):
    global button_registration
    button_registration = player


# initializing games' buttons

chicken = Button(games, all_sprites, pygame.transform.scale(load_image("chickens.png"), (150, 150)))
chicken.press = a

tanks = Button(games, all_sprites, pygame.transform.scale(load_image("tanks.png"), (150, 150)))
tanks.press = b

toads = Button(games, all_sprites, pygame.transform.scale(load_image("toads.png"), (150, 150)))
toads.press = c

ufo = Button(games, all_sprites, pygame.transform.scale(load_image("ufos.png"), (150, 150)))
ufo.press = d

race = Button(games, all_sprites, pygame.transform.scale(load_image("race.png"), (150, 150)))
race.press = e

settings = Button(games, all_sprites, pygame.transform.scale(load_image("gear.png"), (64, 64)))
settings.press = sett


def print_key(image, key):
    font = pygame.font.SysFont('arial', 30)
    text = font.render(keys[key], False, 'black')
    text_x = image.get_rect().w // 2 - text.get_width() // 2
    text_y = image.get_rect().h // 2 - text.get_height() // 2
    image.blit(text, (text_x, text_y))
    return image


first_btn = Button(setting_btns, all_sprites,
                   print_key(pygame.transform.scale(load_image('button_red.png'), (128, 64)), PLAYERONEKEY))
first_btn.press = lambda: btn_change(1)
scnd_btn = Button(setting_btns, all_sprites,
                  print_key(pygame.transform.scale(load_image('button_blu.png'), (128, 64)), PLAYERTWOKEY))
scnd_btn.press = lambda: btn_change(2)

chicken.rect = chicken.rect.move(100, 100)
tanks.rect = tanks.rect.move(300, 100)
toads.rect = toads.rect.move(500, 100)
ufo.rect = ufo.rect.move(100, 300)
race.rect = race.rect.move(300, 300)

settings.rect = settings.rect.move(400 - 32, 500)
first_btn.rect = first_btn.rect.move(150, 200)
scnd_btn.rect = scnd_btn.rect.move(width - 150 - 128, 200)

# initializing settings

# main cycle
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if setting_open and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            setting_open = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not setting_open:
                for b in games.sprites():
                    if b.rect.collidepoint(x, y):
                        b.press()
                        break
            else:
                for b in setting_btns.sprites():
                    if b.rect.collidepoint(x, y):
                        b.press()
                        break
        else:
            if button_registration:
                if event.type == pygame.KEYDOWN:
                    new_btn = event.key
                    if button_registration == 1:
                        PLAYERONEKEY = new_btn
                        first_btn.im_change(
                            print_key(pygame.transform.scale(load_image('button_red.png'), (128, 64)),
                                      PLAYERONEKEY))
                    elif button_registration == 2:
                        PLAYERTWOKEY = new_btn
                        scnd_btn.im_change(
                            print_key(pygame.transform.scale(load_image('button_blu.png'), (128, 64)),
                                      PLAYERTWOKEY))
                    button_registration = 0

    screen.fill((124, 236, 253))
    if not setting_open:
        games.draw(screen)
        all_sprites.update()
    else:
        setting_btns.draw(screen)
        setting_btns.update()
    pygame.display.flip()
pygame.quit()
