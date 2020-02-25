import os
import pygame
import requests


def maps_second_part(cords, scale):
    response = None
    first_scale = scale
    x_cords = float(cords[0])
    y_cords = float(cords[1])
    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    if first_scale < 1:
                        scale += first_scale
                    else:
                        scale += first_scale / 10
                    scale += first_scale / 10
                    if scale >= 65:
                        scale = 65
                elif event.key == pygame.K_PAGEUP:
                    if first_scale < 1:
                        scale -= first_scale
                    else:
                        scale -= first_scale / 10
                    if scale <= 0.1:
                        scale = 0.01
        response = requests.get("http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},{}&l=sat".format(x_cords, y_cords, scale, scale))
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen = pygame.display.set_mode((600, 450))
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        os.remove(map_file)


if __name__ == '__main__':
    print('''
Добро пожаловать в Maps_Api. Для поиска места вам нужно ввести его координаты.
Координаты должны быть введены через пробел и находится в диапозоне -178 до 178 для широты (первого числа)
и от -80 до 80 для долготы (второго числа). Пример: координаты Москвы имеют вид 37.748073 55.658824
Так же во воторой строке вам нужно одним числом ввести масштаб карты в пределах от 0.01 до 65. Оптимальными координатами являются числа от 0.1 до 1.
Пример масштаба: 0.5
        ''')
    cords = input('Введите координаты (через пробел): ').split()
    scale = float(input('Введите масштаб (одно число): '))
    # 45.029903 53.189908 Координаты Пензы
    maps_second_part(cords, scale)
