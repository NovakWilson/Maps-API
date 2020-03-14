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
    screen = pygame.display.set_mode((600, 450))
    text = ''
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(400, 10, 180, 25)
    delete_button = pygame.Rect(500, 40, 50, 25)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    marks = ''
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

                if active:
                    if event.key == pygame.K_RETURN:
                        text = '+'.join(text.split())
                        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={}&format=json".format(text)
                        response = requests.get(geocoder_request)
                        json_response = response.json()
                        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                        codrinates = toponym["Point"]["pos"]
                        x_cords = float(codrinates.split()[0])
                        y_cords = float(codrinates.split()[1])
                        marks += '{},{},pm2wtl~'.format(x_cords, y_cords)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                elif delete_button.collidepoint(event.pos):
                    if len(marks) > 2:
                        marks = '~'.join(marks[:-1].split('~')[:-1]) + '~'
                        print('Метка удалена')
                    else:
                        print('Меток больше нет')
                else:
                    active = False
                color = color_active if active else color_inactive
        response = requests.get("http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},{}&l={}&pt={}".format(x_cords, y_cords, scale, scale, regime, marks[:-1]))
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        txt_surface = font.render(text, True, (0, 0, 0))
        txt_delete = font.render('del', True, (0, 0, 0))
        pygame.draw.rect(screen, color, (400, 10, 200, 25))
        pygame.draw.rect(screen, color, (500, 40, 50, 25))
        screen.blit(txt_surface, (400, 10))
        screen.blit(txt_delete, (510, 40))
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
Для поиска объектов используйте текстовое поле, которое находится в правом верхнем углу.
Для ввода текста нужно нажать на поле. Если название объекта состоит из двух и более слов, вводите их через пробел.
Для осуществления поиска нажмите ENTER.
        ''')
    cords = input('Введите координаты (через пробел): ').split()
    scale = float(input('Введите масштаб (одно число): '))
    while not -180 < float(cords[0]) < 180 or not -80 < float(cords[1]) < 80:
        print('Координаты введены не верно. Попробуйте еще раз.')
        cords = input('Введите координаты (через пробел): ').split()
        scale = float(input('Введите масштаб (одно число): '))
    # 45.029903 53.189908 Координаты Пензы
    maps_fourth_part(cords, scale)
