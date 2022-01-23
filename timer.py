from random import randint
import pygame

pygame.init()
font1 = pygame.font.SysFont('arial', 70)
font2 = pygame.font.SysFont('arial', 15)
font3 = pygame.font.SysFont('arial', 35)
screen = pygame.display.set_mode((800, 600))
PLAYERONEKEY = pygame.K_a
PLAYERTWOKEY = pygame.K_l
kol1 = 0
kol2 = 0
raund = 1
t1 = 0
t2 = 0


def reset():
    global kol1, kol2, raund, time0
    kol1 = 0
    kol2 = 0
    raund = 1


def igra(kol1, kol2, raund, time0):
    screen.fill((5, 205, 45))
    clock = pygame.time.Clock()
    timefinish = randint(10, 20)

    calc = 0
    text = ''
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    text2 = f'Нужно нажать на свою кнопку как можно ближе ко времени: {timefinish}'
    screen.blit(font2.render(text2, True, (0, 0, 0)), (130, 200))

    screen.fill(pygame.Color('blue'), (5, 5, 250, 150))
    screen.blit(font2.render(f'Нажмите на клавишу: a', True, (255, 255, 255)), (17, 53))

    screen.fill(pygame.Color('red'), (545, 445, 250, 150))
    screen.blit(font2.render(f'Нажмите на клавишу: l', True, (255, 255, 255)), (557, 494))

    time1 = '0'
    time2 = '0'

    x1 = 0
    x2 = 0
    dt1 = 0
    dt2 = 0

    running = True
    time0 = round(pygame.time.get_ticks() / 1000, 3)
    while running:
        for e in pygame.event.get():
            screen.blit(font3.render(f'ROUND {raund}', True, (0, 0, 0)), (450, 80))
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    time0 = round(pygame.time.get_ticks() / 1000, 3)
                    running = False
            if e.type == pygame.QUIT:
                running = False
            if not (x1 == 1 and x2 == 1) and not calc == timefinish + 5:
                if e.type == pygame.USEREVENT:
                    calc += 1
                if calc <= timefinish:
                    text = str(calc)
                if calc >= 7:
                    screen.fill(pygame.Color(0, 0, 0), (350, 250, 150, 110))
                else:
                    screen.fill(pygame.Color(5, 205, 45), (300, 250, 200, 110))
                    screen.blit(font1.render(text, True, (0, 0, 0)), (400, 250))
                if e.type == pygame.KEYDOWN:
                    if x1 == 0:
                        if e.key == PLAYERONEKEY:
                            time1 = str(round(pygame.time.get_ticks() / 1000 - time0, 3))
                            x1 += 1
                            dt1 = abs(float(time1) - timefinish)
                    if x2 == 0:
                        if e.key == PLAYERTWOKEY:
                            time2 = str(round(pygame.time.get_ticks() / 1000 - time0, 3))
                            x2 += 1
                            dt2 = abs(float(time2) - timefinish)

            else:
                screen.blit(font2.render(time1, True, (255, 255, 225)), (17, 83))
                screen.blit(font2.render(time2, True, (255, 255, 225)), (557, 524))

                if abs(float(time1) - timefinish) < abs(float(time2) - timefinish):
                    screen.blit(font3.render('ПОЗДРАВЛЯЮ!!!', True, (0, 0, 255)), (15, 390))
                    screen.blit(font3.render('СИНИЙ, ВЫ ВЫИГРАЛИ!', True, (0, 0, 255)), (15, 440))
                    screen.blit(
                        font2.render(f'ВЫ БЛИЖЕ К ЧИСЛУ НА {round(float(time1) - float(time2), 3)} СЕКУНД', True,
                                     (0, 0, 255)), (15, 493))
                    kol1 += 1

                elif abs(float(time2) - timefinish) < abs(float(time1) - timefinish):
                    screen.blit(font3.render('ПОЗДРАВЛЯЮ!!!', True, (255, 0, 0)), (15, 390))
                    screen.blit(font3.render('КРАСНЫЙ, ВЫ ВЫИГРАЛИ!', True, (255, 0, 0)), (15, 440))
                    screen.blit(
                        font2.render(f'ВЫ БЛИЖЕ К ЧИСЛУ НА {round(float(time2) - float(time1), 3)} СЕКУНД', True,
                                     (255, 0, 0)), (15, 493))
                    kol2 += 1

                else:
                    screen.blit(font1.render('НИЧЬЯ', True, (255, 255, 255)), (45, 415))
                    kol1 += 1
                    kol2 += 1
                if e.type == pygame.USEREVENT:
                    calc += 1

        pygame.display.flip()
        clock.tick(60)
    screen.blit(font2.render(time1, True, (0, 0, 0)), (17, 83))
    screen.blit(font2.render(time2, True, (0, 0, 0)), (557, 524))
    return dt1, dt2


def timer_run():
    running = True
    kol1 = 0
    kol2 = 0
    raund = 1
    t1 = 0
    t2 = 0
    time0 = 0
    reset()
    while kol1 < 3 and kol2 < 3:
        dt1, dt2 = igra(kol1, kol2, raund, time0)
        raund += 1
        if dt1 > dt2:
            kol2 += 1
        elif dt1 < dt2:
            kol1 += 1
        else:
            kol1 += 1
            kol2 += 1
        print(kol1, kol2)
