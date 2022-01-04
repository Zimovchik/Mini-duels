import pygame
from math import cos, sin


def tanks_run():
    WIDTH, HEIGHT = 800, 600
    PLAYERONEKEY = pygame.K_SPACE
    PLAYERTWOKEY = pygame.K_UP
    ANGLE_SPEED = 5
    BULLET_SPEED = 30

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

    class Player(pygame.sprite.Sprite):
        def __init__(self, color, player_number):
            super().__init__(char, all_sprites)
            self.pos = WIDTH // 2, HEIGHT // 2
            self.center = WIDTH // 2 + 32, HEIGHT // 2 + 32
            self.color = pygame.Color(color)
            self.image = player_image
            self.angle = 0
            self.mask = pygame.mask.from_surface(self.image)
            self.vx, self.vy = 0, 0
            self.is_alive = True
            self.number = player_number

        def update(self, ticks=0):
            if ticks:
                self.angle += ANGLE_SPEED * ticks / 1000
                if int(self.angle) > 360:
                    self.angle = 1
            # print(self.angle)
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, pygame.Color("grey"), (32, 32), 32, 0)
            pygame.draw.line(self.image, self.color, (32, 32), (32 + cos(self.angle) * 32, 32 + sin(self.angle) * 32),
                             3)

        def shoot(self):
            Bullet(self.angle, (self.center[0] + cos(self.angle) * 32, self.center[1] + sin(self.angle) * 32))

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, angle, pos):
            super().__init__(bullets, all_sprites)
            print(pos, cos(angle), sin(angle))
            self.image = bullet_image
            self.rect = self.image.get_rect()
            self.vx = BULLET_SPEED * cos(angle)
            self.vy = BULLET_SPEED * sin(angle)
            print(self.vx, self.vy)
            self.pos_x, self.pos_y = pos
            self.pos_x -= 4
            self.pos_y -= 4
            self.mask = pygame.mask.from_surface(self.image)

        def update(self, ticks=0):
            if ticks:
                self.pos_x += self.vx * ticks / 1000
                self.pos_y += self.vy * ticks / 1000
            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)
            if self.rect.x + self.rect.w >= WIDTH or self.rect.y + self.rect.h >= HEIGHT:
                self.kill()

    player_image = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
    pygame.draw.circle(player_image, pygame.Color("grey"), (32, 32), 32, 0)
    bullet_image = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
    pygame.draw.circle(bullet_image, pygame.Color("grey"), (8, 8), 8, 0)

    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption('Tanks')
        size = WIDTH, HEIGHT
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        running = True

        all_sprites = pygame.sprite.Group()
        char = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        players = []
        player1 = Player('blue', 1)
        players.append(player1)

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
                #     if event.key == PLAYERTWOKEY:
                #         player2.shoot()
            tick_passed = clock.tick()
            all_sprites.update(tick_passed)
            for i in players:
                screen.blit(i.image, (WIDTH // 2, HEIGHT // 2))
            for i in bullets:
                screen.blit(i.image, (i.rect.x, i.rect.y))
            pygame.display.flip()
