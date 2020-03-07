import os
import pygame
import requests


def maps_fourth_part(cords, scale):
    response = None
    regime = 'map'
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
                elif event.key == pygame.K_UP:
                    y_cords += 0.5
                    if y_cords >= 80:
                        y_cords = 80
                elif event.key == pygame.K_DOWN:
                    y_cords -= 0.5
                    if y_cords <= -80:
                        y_cords = -80
                elif event.key == pygame.K_RIGHT:
                    if x_cords >= 179:
                        x_cords = -179
                    x_cords += 0.5
                elif event.key == pygame.K_LEFT:
                    x_cords -= 0.5
                    if x_cords <= -179:
                        x_cords = 179

                elif event.key == pygame.K_1:
                    regime = 'map'
                elif event.key == pygame.K_2:
                    regime = 'sat'
                elif event.key == pygame.K_3:
                    regime = 'sat,skl'

        response = requests.get("http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},{}&l={}".format(x_cords, y_cords, scale, scale, regime))
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
Для переключения режима карты используются кнопки '1'(для схемы), '2'(для спутника) и '3'(для гибрида).
        ''')
    cords = input('Введите координаты (через пробел): ').split()
    scale = float(input('Введите масштаб (одно число): '))
    while not cords[0].isdigit() or not cords[1].isdigit() or \
            not -180 < float(cords[0]) < 180 or not -80 < float(cords[1]) < 80:
        print('Координаты введены не верно. Попробуйте еще раз.')
        cords = input('Введите координаты (через пробел): ').split()
        scale = float(input('Введите масштаб (одно число): '))
    # 45.029903 53.189908 Координаты Пензы
    maps_fourth_part(cords, scale)
