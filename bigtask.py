import pygame
import requests
import sys
import os

spn = input()
cord1, cord2 = input().split()


def moove(arrow):
    global spn, cord1, cord2
    if arrow == 'left':
        cord1 = float(cord1)
        cord1 -= (float(spn) * 2)
        cord1 = str(cord1)
    elif arrow == 'right':
        cord1 = float(cord1)
        cord1 += (float(spn) * 2)
        cord1 = str(cord1)
    elif arrow == 'forward':
        cord2 = float(cord2)
        cord2 += (float(spn) * 2)
        cord2 = str(cord2)
    elif arrow == 'back':
        cord2 = float(cord2)
        cord2 -= (float(spn) * 2)
        cord2 = str(cord2)
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},0.002&l=map".format(cord1, cord2, spn)
    response = requests.get(map_request)
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)


def scaale(znak):
    global spn, cord1, cord2
    if znak == '+':
        spn = float(spn) + 0.01
        spn = str(spn)
    elif znak == '-':
        if float(spn) > 0.01:
            spn = float(spn) - 0.01
            spn = str(spn)
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},0.002&l=map".format(cord1, cord2, spn)
    response = requests.get(map_request)
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)


response = None
# coords = 37.530887, 55.703118

try:
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},0.002&l=map".format(cord1, cord2, spn)
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
        if event.type == pygame.KEYDOWN and event.key == 276 and event.scancode == 75:
            moove('left')
        if event.type == pygame.KEYDOWN and event.key == 275 and event.scancode == 77:
            moove('right')
        if event.type == pygame.KEYDOWN and event.key == 273 and event.scancode == 72:
            moove('forward')
        if event.type == pygame.KEYDOWN and event.key == 274 and event.scancode == 80:
            moove('back')
        if event.type == pygame.KEYDOWN and event.key == 280 and event.scancode == 73:
            scaale('+')
        if event.type == pygame.KEYDOWN and event.key == 281 and event.scancode == 81:
            scaale('-')
        if event.type == pygame.QUIT:
            running = False
# Рисуем картинку, загружаемую из только что созданного файла.
# Переключаем экран и ждем закрытия окна.
# pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
