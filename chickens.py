import pygame
import sys
import random as rnd

CLK = 70
pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("data/background.png").convert()
WIDTH, HEIGHT = 800, 600

platforms_sprites = pygame.sprite.Group()
chicken_sprites = pygame.sprite.Group()


class Chicken(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(chicken_sprites)
        self.add(chicken_sprites)
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.can_jump = True
        self.goes_up = True


class Object(pygame.sprite.Sprite):
    #  Это платформы, по которым прыгают
    def __init__(self, x, y, width, height):
        super().__init__(platforms_sprites)
        self.add(platforms_sprites)
        self.image = pygame.Surface([width, height])
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(self.image, (255, 0, 0),
                         (self.rect[0], self.rect[1], self.rect[2], self.rect[3]),
                         width=0)


def run():
    chick = Chicken(50, 400)

    objects = [Object(0, 464, 400, 20), Object(0, 50, 400, 20)]

    while True:
        clock.tick(CLK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    chick.move()
        screen.fill("white")
        platforms_sprites.update()
        platforms_sprites.draw(screen)
        chicken_sprites.update()
        chicken_sprites.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    clock = pygame.time.Clock()

    run()
    pygame.quit()
