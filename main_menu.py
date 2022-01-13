import os
import sys
import pygame

# from tanks import tanks_run
# from toads import toads_run
from chickens import chickens_run

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
# sprite groups

all_sprites = pygame.sprite.Group()
games = pygame.sprite.Group()
setting_btns = pygame.sprite.Group()

# window control vars
running = True
setting_open = False
volume_on = False
button_registration = False
player_number = 0
new_btn = None
PLAYERONEKEY = pygame.K_SPACE
PLAYERTWOKEY = pygame.K_UP


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
    # chickens_run()


def b():  # tanks btn func
    print('tanks')
    # tanks_run()


def c():  # toads btn func
    print("toads")
    # toads_run()


def open_settings():
    global setting_open
    setting_open = True


def close_settings():
    global setting_open
    setting_open = False


def p1bind_change():
    global button_registration
    global player_number
    player_number = 1
    button_registration = True


def p2bind_change():
    global button_registration
    global player_number
    player_number = 2
    button_registration = True


def volume_change(btn=None):
    global volume_on
    global volume
    if volume_on:
        volume.im_change(pygame.transform.scale(load_image("volumeoff.png"), (100, 100)))
    else:
        volume.im_change(pygame.transform.scale(load_image("volume.png"), (100, 100)))
    volume_on = not volume_on


# initializing games' buttons

chicken = Button(games, all_sprites, pygame.transform.scale(load_image("chickens.png"), (150, 150)))
chicken.press = a
tanks = Button(games, all_sprites, pygame.transform.scale(load_image("tanks.png"), (150, 150)))
tanks.press = b
toads = Button(games, all_sprites, pygame.transform.scale(load_image("toads.png"), (150, 150)))
toads.press = c
settings = Button(games, all_sprites, pygame.transform.scale(load_image("settings.png"), (50, 50)))
settings.press = open_settings
chicken.rect = chicken.rect.move(100, 100)
tanks.rect = tanks.rect.move(300, 100)
toads.rect = toads.rect.move(500, 100)
settings.rect = settings.rect.move(750, 550)

# initializing settings

volume = Button(setting_btns, all_sprites, pygame.transform.scale(load_image("volume.png"), (100, 100)))
volume.press = volume_change
volume.rect = volume.rect.move(100, 100)

back_btn = Button(setting_btns, all_sprites, pygame.transform.scale(load_image("back_btn.png"), (50, 50)))
back_btn.press = close_settings
# Changing player button binds

player1_btn_bind = Button(setting_btns, all_sprites,
                          pygame.transform.scale(load_image("p1bind-change.png"), (100, 100)))
player2_btn_bind = Button(setting_btns, all_sprites,
                          pygame.transform.scale(load_image("p2bind-change.png"), (100, 100)))
# main cycle
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not setting_open:
                for b in games.sprites():
                    if b.rect.collidepoint(x, y):
                        b.press()
                        break
            else:
                if button_registration:
                    if event.type == pygame.KEYDOWN:
                        new_btn = event.key
                        if player_number == 1:
                            PLAYERONEKEY = new_btn
                        elif player_number == 2:
                            PLAYERTWOKEY = new_btn
                        button_registration = False
                        player_number = 0
                for b in setting_btns.sprites():
                    if b.rect.collidepoint(x, y):
                        b.press()
                        break
    screen.fill((124, 236, 253))
    if not setting_open:
        games.draw(screen)
        all_sprites.update()
    else:
        setting_btns.draw(screen)
        setting_btns.update()
    pygame.display.flip()
pygame.quit()
