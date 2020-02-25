import os
import pygame
import requests
import sys


def maps_first_part(cords, scale):
    response = None
    x_cords = float(cords[0])
    y_cords = float(cords[1])
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},{}&l=sat".format(x_cords, y_cords, scale, scale)
    # map_request = "http://static-maps.yandex.ru/1.x/?ll=141.378618,-26.316922&spn=34,34&l=sat".format(x_cords, y_cords, scale, scale)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    cords = input('Введите координаты: ').split()
    scale = float(input('Введите масштаб: '))
    maps_first_part(cords, scale)
