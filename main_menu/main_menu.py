import os
import sys
#system libs
import pygame

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
games = pygame.sprite.Group()
running = True


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


chicken = Button(games, all_sprites, load_image("images/chickens.png"))
tanks = Button(games, all_sprites, load_image("images/tanks.png"))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()