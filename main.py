import random

import pygame
import render

pygame.init()

display_w = 800
display_h = 600
display = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('Python Dino | v1.0')
logo = pygame.image.load('resources/logo.png')
pygame.display.set_icon(logo)

cactus_img = [pygame.image.load('resources/gameFiles/Cactus0.png'), pygame.image.load('resources/gameFiles/Cactus1.png'), pygame.image.load('resources/gameFiles/Cactus2.png')]
cactus_options = [69, 449, 37, 410, 80, 420]
stone_img = [pygame.image.load('resources/gameFiles/Stone0.png'), pygame.image.load('resources/gameFiles/Stone1.png')]
cloud_img = [pygame.image.load('resources/gameFiles/Cloud0.png'), pygame.image.load('resources/gameFiles/Cloud0.png')]

dino_img = [pygame.image.load('resources/Dino/Dino0.png'), pygame.image.load('resources/Dino/Dino1.png'), pygame.image.load('resources/Dino/Dino2.png'), pygame.image.load('resources/Dino/Dino3.png'), pygame.image.load('resources/Dino/Dino4.png')]
img_counter = 0
class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            self.x = display_w + 100 + random.randrange(-80, 60)
            return False

    def return_selfcactus(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))



player_w = 60
player_h = 100
player_x = display_w // 3
player_y = display_h - player_h - 100
cactus_w = 20
cactus_h = 70
cactus_x = display_w - 50
cactus_y = display_h - cactus_h - 100

clock = pygame.time.Clock()

make_jump = False
jump_count = 30

def run_game():
    global make_jump
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    stone, cloud = open_random_object()

    array = cactus_arr  # Define the array variable here
    land = pygame.image.load('resources/bg.png')

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        display.blit(land, (0, 0))
        move_objects(stone, cloud)
        draw_array(array)

        draw_dino()

        if check_collision(cactus_arr):
            game = False


        pygame.display.update()
        clock.tick(70)

    return GameOver()



def jump():
    global player_y, jump_count, make_jump
    if jump_count >= -30:
        player_y -= jump_count / 2.5
        jump_count -= 1
    else:
        jump_count = 30
        make_jump = False

def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_w + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_w + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_w + 600, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)
    if maximum < display_w:
        radius = display_w
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)
    return radius



def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_selfcactus(radius, height, width, img)

def open_random_object():
    choice = random.randrange(0, 2)
    image_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    image_cloud = cloud_img[choice]

    stone = Object(display_w, display_h - 80, 10, image_stone, 4)
    cloud = Object(display_w, 80, 70, image_cloud, 2)

    return stone, cloud

def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        image_stone = stone_img[choice]
        stone.return_selfcactus(display_w, 500 + random.randrange(10, 80), stone.width, image_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        image_cloud = cloud_img[choice]
        cloud.return_selfcactus(display_w, random.randrange(10, 200), stone.width, image_cloud)


def draw_dino():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img[img_counter // 5], (player_x, player_y))
    img_counter += 1

def print_text(message, x, y, font_color = (0, 0, 0), font='resources/font/font.ttf', font_size = 30):
    font = pygame.font.Font(font, font_size)
    text = font.render(message, True, font_color)
    display.blit(text, (x, y))

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Игра на паузе! Нажми Enter для продолжения.', 100, 270)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)

def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 449:
            if not make_jump:
                if barrier.x <= player_x + player_w - 22 <= barrier.x + barrier.width:
                        return True
            elif jump_count >= 0:
                if player_y + player_h - 5 >= barrier.y:
                    if barrier.x <= player_x + player_w - 22 <= barrier.x + barrier.width:
                        return True
            else:
                if player_y + player_h - 10 >= barrier.y:
                    if barrier.x <= player_x <= barrier.x + barrier.width:
                        return True
        else:
            if not make_jump:
                if barrier.x <= player_x + player_w + 5 <= barrier.x + barrier.width:
                    return True
            elif jump_count == 10:
                if player_y + player_h - 5 >= barrier.y:
                    if barrier.x <= player_x + player_w - 5 <= barrier.x + barrier.width:
                        return True
            elif jump_count <= 1:
                if player_y + player_h - 2 >= barrier.y:
                    if barrier.x <= player_x + 13 <= barrier.x + barrier.width:
                        return True
            elif jump_count >= 1:
                if player_y + player_h - 2 >= barrier.y:
                    if barrier.x <= player_x + player_w - 22 <= barrier.x + barrier.width:
                        return True
            else:
                if player_y + player_h - 3 >= barrier.y:
                    if barrier.x <= player_x + player_w + 5 <= barrier.x + barrier.width:
                        return True
    return False

def GameOver():
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Вы проиграли! Нажми Enter для продолжения', 100, 270)
        print_text('Или Esc для выхода', 300, 310)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)

while run_game():
    pass
pygame.quit()
quit()