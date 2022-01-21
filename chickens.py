import pygame, os, sys, random
from PIL import Image


# Объявляем переменные
WIDTH = 800  # Ширина создаваемого окна
HEIGHT = 600  # Высота
DISPLAY = (WIDTH, HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
PLAYER_SIZE = 64  # Размеры игрока
TILE_SIZE = 16  # Размер клеток платформ (.)
P1_BUTTON, P2_BUTTON = pygame.K_a, pygame.K_l  # Кнопки, отвечающие за игроков
SPEED = 2  # Скорость движения всей системы
GRAVITY = 10

all_sprites = pygame.sprite.Group()  # Группы спрайтов
platforms_sprites = pygame.sprite.Group()
chicken_sprites = pygame.sprite.Group()
finish_sprites = pygame.sprite.Group()

chicken_pic1 = 'anime chicken1.png'  # Два варианта есть в принципе в папке data
chicken_pic2 = 'anime chicken2.png'
platform_pic = 'block.png'  # Тоже есть несколко вариантов, но этот лучший
background_pic = ''
finish_image = 'finish.png'

pygame.init()
screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
pygame.display.set_caption("Chickens")
bg = pygame.Surface((WIDTH, HEIGHT))  # Создание видимой поверхности (фон)
bg.fill(pygame.Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом


def chickens_run():

    def load_image(name, colorkey=None, is_plat=0):  # Обрабатывающая картинки функция
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
        new_players, objects, x, y, finish = [], [], None, None, []
        player_count = 1

        counter = 0
        first_platform_x = 0
        first_platform_y = 0
        for y in range(len(level)):
            for x in range(1, len(level[y])):
                if level[y][x] == '-' and level[y][x - 1] != '-':
                    first_platform_x, first_platform_y = x * 16, y * 16
                    counter = 1  # Запоминаем длинy платформы пока не кончится
                elif x + 1 <= len(level[y]) - 1 and level[y][x] == '-' and level[y][x + 1] != '-':
                    counter += 1
                    objects.append(Platforms(first_platform_x, first_platform_y, counter))
                elif level[y][x] == '-':
                    counter += 1
                elif level[y][x] == '@':  # Игрок в 2 раза больше клеток
                    new_players.append(Chicken(x * 16, y * 16, player_count))
                    player_count += 1
                elif level[y][x] == '=':
                    finish.append(Finish(x * 16, y * 16))

        # вернем игрока, а также размер поля в клетках
        return new_players, objects, x, y, finish

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
            self.vx = SPEED

        def move(self):
            self.rect[0] += self.vx

    def endgame(lost_player_num):
        pass

    class Chicken(pygame.sprite.Sprite):  # Класс курицы (игрока)
        image1 = load_image(chicken_pic1)  # Картинка первого игрока
        image1 = pygame.transform.scale(image1, (PLAYER_SIZE, PLAYER_SIZE))

        image2 = load_image(chicken_pic2)  # Второго
        image2 = pygame.transform.scale(image2, (PLAYER_SIZE, PLAYER_SIZE))

        def __init__(self, x, y, count):
            super().__init__(chicken_sprites)
            self.add(chicken_sprites)
            self.add(all_sprites)

            self.player_number = count  # Номер игрока
            if count == 1:
                self.image = Chicken.image1  # Загрузка соответствующих изображений
                self.rect = self.image.get_rect()  # Размеры
                self.rect.x, self.rect.y = x, y
            elif count == 2:
                self.image = Chicken.image2
                self.rect = self.image.get_rect()  # Размеры
                self.rect.x, self.rect.y = x, y

            self.gravity = GRAVITY

            self.vx = SPEED  # Дефолтная скорость движения по иксу (равна скорости камеры)
            # Возможно изменение при контакте с платформами сбоку
            self.vy = 0  # В начале равна 0, изменяется при смене гравитации
            self.posX, self.posY = x, y
            self.canJump = True
            self.isAlive = True
            self.isOnGround = False  # Стоит ли непосредственно на поверхности
            self.goesDown = True  # Летит ли игрок вниз

        def update(self, time=0):
            # Игрок на самом окне не двигается, двигается мир вокруг него
            if self.goesDown:  # Если сейчас время падать вниз
                if not self.isOnGround:  # если летит
                    self.vy += self.gravity * time / 1000
                self.isOnGround = False
                self.rect.y += self.vy  # Плюс гравитация и проверка на столкновение
                self.collide(0, self.vy, platforms_sprites)
            else:  # То же самое но для подъема вверх
                if not self.isOnGround:
                    self.vy += self.gravity * time / 1000
                self.isOnGround = False
                self.rect.y += self.vy
                self.collide(0, self.vy, platforms_sprites)

        def collide(self, vx, vy, platforms):
            for p in platforms:
                if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                    w_collide_d, h_collide_d = self.get_collide_rect_down(p)
                    # ширина и высота прямоугольника пересечения

                    if h_collide_d >= w_collide_d:  # если пересекается справа
                        self.rect.right = p.rect.left  # то останавливается
                        self.vx = -SPEED
                        #self.isOnGround = True
                        self.canJump = True
                    elif vy > 0:  # если падает вниз
                        self.rect.bottom = p.rect.top  # то не падает вниз
                        self.canJump = True  # и может прыгать дальше
                        self.isOnGround = True
                        self.vy = 0
                    elif vy < 0:  # если "падает" вверх
                        self.rect.top = p.rect.bottom  # то не "падает" вверх
                        self.canJump = True
                        self.isOnGround = True
                        self.vy = 0  # и энергия прыжка пропадает
            if not self.rect.colliderect(screen_rect):  # проверка на смерть-выход за границы экрана
                self.kill()
                self.isAlive = False # игрок умирает а все в игре останавливается
                camera.vx = 0
                for fin in finishes:
                    fin.vx = 0
                self.stop_another_player(self.player_number)
                for plat in platforms_sprites:
                    plat.vx = 0
                endgame(self.player_number)  # финальный экран подведения итогов

        def get_collide_rect_down(self, plat):
            w = PLAYER_SIZE - (plat.rect.x - self.rect.x)
            if self.rect.y <= plat.rect.y:
                h = TILE_SIZE
            else:
                h = TILE_SIZE - (plat.rect.y - self.rect.y)
            return w, h

        def get_collide_rect_up(self, plat):
            w = PLAYER_SIZE - (plat.rect.x - self.rect.x)
            if self.rect.y + PLAYER_SIZE >= plat.rect.y + TILE_SIZE:
                h = TILE_SIZE
            else:
                h = TILE_SIZE - (plat.rect.y - self.rect.y)
            return w, h

        def change_gravity(self, time=0):
            if not self.canJump:  # если прыжок невозможен
                return
            if self.goesDown:
                self.goesDown = False
            else:
                self.goesDown = True
            self.image = pygame.transform.flip(self.image, False, True)  # картинку вверх тормашками
            self.gravity = -self.gravity
            self.canJump = False

        def stop_another_player(self, your_num):
            if your_num == 1:
                player2.vx = 0
                player2.vy = 0
                player2.gravity = 0
                player2.isOnGround = False
                player2.canJump = False
            elif your_num == 2:
                player1.vx = 0
                player1.vy = 0
                player1.gravity = 0
                player1.isOnGround = False
                player1.canJump = False

        def get_pos(self):
            return self.posX, self.posY

        def get_rect(self):
            return self.rect

        def get_player_number(self):
            return self.player_number

    def load_platform(name, len_pl):
        '''Отдельная ф-я для создания картинки платформы'''
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        res = Image.new('RGB', (64 * len_pl, 64))
        block = Image.open(fullname)
        for i in range(len_pl):
            res.paste(block, (i * 64, 0))
        res_name = os.path.join('data', 'platfrom_res.png')
        res.save(res_name)
        return res_name

    class Platforms(pygame.sprite.Sprite):
        #  Это платформы, по которым прыгают
        def __init__(self, x, y, plat_len):
            super().__init__(platforms_sprites)
            self.add(platforms_sprites)
            self.add(all_sprites)

            print(plat_len)
            name = load_platform(platform_pic, plat_len)
            # название файла с изображением готов платформы нужной длинны
            image = pygame.image.load(name)
            # загрузка этой самой картинки через основную ф-ю загрузки пикч
            self.image = pygame.transform.scale(image, (plat_len * TILE_SIZE, TILE_SIZE))
            os.remove(name)  # удаляю платформу
            self.rect = self.image.get_rect()  # Размеры
            self.rect.x, self.rect.y = x, y
            self.vx = -SPEED  # движется в другую сторону

        def draw(self):
            self.rect[0] += self.vx

    class Finish(pygame.sprite.Sprite):
        # финиш, игра заканчивается
        image = load_image(finish_image)

        def __init__(self, x, y):
            super().__init__(finish_sprites)
            self.add(all_sprites)
            self.add(finish_sprites)

            self.image = Finish.image
            self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            self.vx = -SPEED

        def draw(self):
            self.rect[0] += self.vx

        def check_ending(self):
            if pygame.sprite.spritecollideany(self, chicken_sprites):
                w_player = pygame.sprite.spritecollideany(self, chicken_sprites)
                if w_player.rect.x >= self.rect.x:
                    w_player.stop_another_player(w_player.player_number)
                    for plat in platforms_sprites:
                        plat.vx = 0
                    camera.vx = 0
                    for fin in finishes:
                        fin.vx = 0
                    endgame(w_player.player_number)  # финальный экран подведения итогов



    screen_rect = (0, 0, WIDTH, HEIGHT)
    camera = Camera(0, 0)
    players, objects, level_x, level_y, finishes = generate_level(load_level('chicken_map'))
    player1, player2 = players
    print(len(objects))

    def main():
        while True:  # Основной цикл программы
            time_passed = clock.tick(60)

            for event in pygame.event.get():  # Обрабатываем события
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == P1_BUTTON:  # При нажатии на кнопку первого игрока
                        player1.change_gravity(
                            time_passed)  # Пытаемся менять гравитацию если это возможно
                    if event.key == P2_BUTTON:  # При нажатии на кнопку второго игрока
                        player2.change_gravity(time_passed)  # То ж самое
            camera.move()
            for obj in objects:
                obj.draw()

            screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
            all_sprites.draw(screen)
            player1.update(time_passed)
            player2.update(time_passed)
            for fin in finishes:
                fin.draw()
                fin.check_ending()

            chicken_sprites.draw(screen)  # Отрисовка спрайтов
            platforms_sprites.draw(screen)
            pygame.display.update()  # обновление и вывод всех изменений на экран
            # pygame.time.wait(30)

    clock = pygame.time.Clock()
    main()