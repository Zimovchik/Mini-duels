import pygame, os, sys, random


def chickens_run():
    pass


# Объявляем переменные
WIDTH = 800  # Ширина создаваемого окна
HEIGHT = 600  # Высота
DISPLAY = (WIDTH, HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 30  # Толщина платформы
PLATFORM_COLOR = "#FF6262"
PLAYER_SIZE = 64  # Размеры игрока
P1_BUTTON, P2_BUTTON = pygame.K_a, pygame.K_l

platforms_sprites = pygame.sprite.Group()
chicken_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):  # Обрабатывающая картинки функция
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Chicken(pygame.sprite.Sprite):  # Класс курицы (игрока)
    '''image = load_image("chicken.png")
    image = pygame.transform.scale(image, (PLAYER_SIZE, PLAYER_SIZE))'''

    def __init__(self, x, y):
        super().__init__(chicken_sprites)
        self.add(chicken_sprites)

        self.image = Chicken.image
        self.rect = self.image.get_rect()  # Размеры
        self.rect.x, self.rect.y = x, y

        self.vx = 0  # Дефолтная скорость движения по иксу (стоит, двигается окружение)
        # Возможно изменение при контакте с платформами сбоку
        self.vy = 0  # В начале равна 0, изменяется при нажатии
        self.posX, self.posY = x, y
        self.canJump = True
        self.isAlive = True
        self.goesUp = True  # Летит ли игрок при след нажатии вверх

    def change_gravity(self):
        if not self.canJump:  # если прыжок невозможен
            return


class Platforms(pygame.sprite.Sprite):
    #  Это платформы, по которым прыгают
    def __init__(self, x, y, plat_len):
        super().__init__(platforms_sprites)
        self.add(platforms_sprites)
        self.image = pygame.Surface([plat_len, PLATFORM_WIDTH], pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('black'), (x, y, plat_len, PLATFORM_WIDTH))
        self.rect = self.image.get_rect()


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Chickens")
    bg = pygame.Surface((WIDTH, HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(pygame.Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    while True:  # Основной цикл программы
        player1 = Chicken(50, 50)
        player2 = None

        platform1 = Platforms(20, 20, 600)
        platform2 = Platforms(20, 300, 600)
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == pygame.QUIT:
                quit()
            if event.type == P1_BUTTON:  # При нажатии на кнопку первого игрока
                player1.change_gravity()  # Пытаемся менять гравитацию если это возможно
            if event.type == P2_BUTTON:  # При нажатии на кнопку второго игрока
                player2.change_gravity()  # То ж самое
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        chicken_sprites.draw(screen)  # Отрисовка спрайтов
        platforms_sprites.draw(screen)
        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()