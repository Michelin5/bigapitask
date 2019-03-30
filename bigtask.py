import pygame
import requests
import sys
import os

# границы cord1 = -174, 174
# границы cord2 = -50, 70

# spisok = ['sat', 'map', 'trf]
# print(','.join(spisok))
filtr = 'sat'
spn = input()
cord1, cord2 = input().split()


# КНОПКИ СЛОЕВ: 1 - СПУТНИК, 2 - СХЕМА, 3 - ГИБРИД

def filteer(key):
    global filtr
    if key == '1':
        filtr = 'sat'
    elif key == '2':
        filtr = 'map'
    elif key == '3':
        filtr = 'sat,skl'
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},0.002&l={}".format(cord1, cord2, spn,
                                                                                        filtr)
    response = requests.get(map_request)
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)


def moove(arrow):
    global spn, cord1, cord2
    if arrow == 'left':
        cord1 = float(cord1)
        if cord1 - (float(spn) * 2) < -174:
            cord1 = (cord1 - (float(spn) * 2))
            while cord1 > 174 or cord1 < -174:
                cord1 += 174
        else:
            cord1 -= (float(spn) * 2)
        cord1 = str(cord1)
    elif arrow == 'right':
        cord1 = float(cord1)
        if cord1 + (float(spn) * 2) > 174:
            cord1 = (cord1 + (float(spn) * 2))
            while cord1 > 174 or cord1 < -174:
                cord1 -= 174
        else:
            cord1 += (float(spn) * 2)
        cord1 = str(cord1)
    elif arrow == 'forward':
        cord2 = float(cord2)
        if cord2 + (float(spn) * 2) > 70:
            cord2 = (cord2 + (float(spn) * 2))
            while cord2 < -50 or cord2 > 70:
                cord2 -= 70
        else:
            cord2 += (float(spn) * 2)
        # cord2 += (float(spn) * 2)
        cord2 = str(cord2)
    elif arrow == 'back':
        cord2 = float(cord2)
        if cord2 - (float(spn) * 2) < -50:
            cord2 = (cord2 - (float(spn) * 2))
            while cord2 < -50 or cord2 > 70:
                cord2 += 50
        else:
            cord2 -= (float(spn) * 2)
        # cord2 -= (float(spn) * 2)
        cord2 = str(cord2)
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},0.002&l={}".format(cord1, cord2, spn,
                                                                                        filtr)
    response = requests.get(map_request)
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)


def scaale(znak):
    global spn, cord1, cord2
    if znak == '+':
        if float(spn) < 131:
            spn = float(spn) * 2
        spn = str(spn)
    elif znak == '-':
        if float(spn) > 0.004:
            spn = float(spn) / 2
            spn = str(spn)
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},0.002&l={}".format(cord1, cord2, spn, filtr)
    response = requests.get(map_request)
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)


response = None
# coords = 37.530887 55.703118

try:
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},0.002&l={}".format(cord1, cord2, spn, filtr)
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
except:
    print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
try:
    with open(map_file, "wb") as file:
        file.write(response.content)
except IOError as ex:
    print("Ошибка записи временного файла:", ex)
    sys.exit(2)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
counter = 0
while running:
    if counter == 0:
        screen.blit(pygame.image.load(map_file), (0, 0))
        counter = 1
        pygame.display.flip()
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            filteer('1')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            filteer('2')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            filteer('3')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            moove('left')
            # print(cord1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            moove('right')
            # print(cord1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            moove('forward')
            # print(cord2)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            moove('back')
            # print(cord2)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            scaale('+')
            # print(cord1, spn)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            scaale('-')
        if event.type == pygame.QUIT:
            running = False
# Рисуем картинку, загружаемую из только что созданного файла.
# Переключаем экран и ждем закрытия окна.
# pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
