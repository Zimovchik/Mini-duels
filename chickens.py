import pygame, os, sys, random


def chickens_run():
    pass


# Объявляем переменные
WIDTH = 800  # Ширина создаваемого окна
HEIGHT = 600  # Высота
DISPLAY = (WIDTH, HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
PLAYER_SIZE = 128  # Размеры игрока
TILE_SIZE = 64  # Размер клеток платформ (.)
P1_BUTTON, P2_BUTTON = pygame.K_a, pygame.K_l  # Кнопки, отвечающие за игроков
SPEED = 3  # Скорость движения всей системы
GRAVITY = 0.2

platforms_sprites = pygame.sprite.Group()
chicken_sprites = pygame.sprite.Group()

chicken_pic = 'anime chicken1.png'  # Два варианта есть в принципе в папке data
platform_pic = 'block.png'  # Тоже есть несколко вариантов, но этот лучший
background_pic = ''  # Пока не выбрали

pygame.init()
screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
pygame.display.set_caption("Chickens")
bg = pygame.Surface((WIDTH, HEIGHT))  # Создание видимой поверхности
# будем использовать как фон
bg.fill(pygame.Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом


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


def generate_level(level):
    new_player, objects, x, y = None, [], None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '-':
                objects.append(Platforms(x * 64, y * 64, 64))
            elif level[y][x] == '@':  # Игрок в 2 раза больше клеток
                new_player = Chicken(x * 64, y * 64)
    # вернем игрока, а также размер поля в клетках
    return new_player, objects, x, y


def load_level(filename):
    filename = "data/maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Camera:  # камера экрана
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 800, 600)

    def move(self):
        self.rect[0] += SPEED


class Chicken(pygame.sprite.Sprite):  # Класс курицы (игрока)
    image = load_image(chicken_pic)
    image = pygame.transform.scale(image, (PLAYER_SIZE, PLAYER_SIZE))

    def __init__(self, x, y):
        super().__init__(chicken_sprites)
        self.add(chicken_sprites)

        self.image = Chicken.image
        self.rect = self.image.get_rect()  # Размеры
        self.rect.x, self.rect.y = x, y

        self.vx = SPEED  # Дефолтная скорость движения по иксу (равна скорости камеры)
        # Возможно изменение при контакте с платформами сбоку
        self.vy = 0  # В начале равна 0, изменяется при смене гравитации
        self.posX, self.posY = x, y
        self.canJump = True
        self.isAlive = True
        self.goesUp = True  # Летит ли игрок при след нажатии вверх

    def move(self):
        # self.rect[0] += SPEED
        self.rect[1] += self.vy

    def update(self):
        # Игрок на самом окне не двигается, двигается мир вокруг него
        for spr in platforms_sprites:
            if pygame.sprite.collide_mask(self, spr):
                self.vy = 0
                break
        self.vy += GRAVITY

    def change_gravity(self):
        if not self.canJump:  # если прыжок невозможен
            return


class Platforms(pygame.sprite.Sprite):
    #  Это платформы, по которым прыгают
    image = load_image(platform_pic)
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def __init__(self, x, y, plat_len):
        super().__init__(platforms_sprites)
        self.add(platforms_sprites)

        self.image = Platforms.image
        self.rect = self.image.get_rect()  # Размеры
        self.rect.x, self.rect.y = x, y

    def draw(self):
        #  Чтобы отрисовка соответствовала позиции камеры его нужно отрисовывать
        #  на self.rect[0]-camera.rect[0], self.rect[1]-camera.rect[1]
        self.rect[0] -= SPEED


camera = Camera(0, 0)
player1, objects, level_x, level_y = generate_level(load_level('chicken_map'))


def main():
    while True:  # Основной цикл программы
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == P1_BUTTON:  # При нажатии на кнопку первого игрока
                    player1.change_gravity()  # Пытаемся менять гравитацию если это возможно
                if event.key == P2_BUTTON:  # При нажатии на кнопку второго игрока
                    player2.change_gravity()  # То ж самое
        player1.move()
        camera.move()
        for obj in objects:
            obj.draw()
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        chicken_sprites.draw(screen)  # Отрисовка спрайтов
        platforms_sprites.draw(screen)
        player1.update()
        pygame.display.update()  # обновление и вывод всех изменений на экран
        pygame.time.wait(30)


if __name__ == "__main__":
    main()
