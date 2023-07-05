import random

import pygame
import render

pygame.init()

display_w = 800
display_h = 600
display = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('Python Dino | v1.1')
logo = pygame.image.load('resources/logo.png')
pygame.display.set_icon(logo)
pygame.mixer_music.load('resources/sounds/background.mp3')
pygame.mixer_music.set_volume(0.5)
loss = pygame.mixer.Sound('resources/sounds/loss.wav')
hp_sound = pygame.mixer.Sound('resources/sounds/hp+.wav')

health_image = pygame.image.load('resources/gameStats/heart.png')
health_image = pygame.transform.scale(health_image, (50, 50))

cactus_img = [pygame.image.load('resources/gameFiles/Cactus0.png'), pygame.image.load('resources/gameFiles/Cactus1.png'), pygame.image.load('resources/gameFiles/Cactus2.png')]
cactus_options = [69, 449, 37, 410, 80, 420]
stone_img = [pygame.image.load('resources/gameFiles/Stone0.png'), pygame.image.load('resources/gameFiles/Stone1.png')]
cloud_img = [pygame.image.load('resources/gameFiles/Cloud0.png'), pygame.image.load('resources/gameFiles/Cloud0.png')]

dino_img = [pygame.image.load('resources/Dino/Dino0.png'), pygame.image.load('resources/Dino/Dino1.png'), pygame.image.load('resources/Dino/Dino2.png'), pygame.image.load('resources/Dino/Dino3.png'), pygame.image.load('resources/Dino/Dino4.png')]
img_counter = 0

def show_health():
    global health
    show = 0
    x = 30
    while show != health:
        display.blit(health_image, (x, 20))
        x += 60
        show += 1

def check_health():
    global health
    health -= 1
    if health == 0:
        pygame.mixer.Sound.play(loss)
        return False
    else:
        return True




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


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (197, 255, 143)
        self.active_color = (152, 245, 66)

    def draw(self, x, y, text, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.time.delay(800)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                     action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))

        print_text(message=text, x=x+20, y=y+3, font_size=font_size)





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
score = 0
maxScore = 0
max_above = 0
health = 3



def show_menu():
    pygame.mixer_music.pause()
    menu_bg = pygame.image.load('resources/menu.png')

    start_button = Button(280, 70)
    quit_button = Button(350, 70)


    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_bg, (0, 0))
        start_button.draw(100, 410, "Начать игру", start_game, 45)
        quit_button.draw(400, 410, "Закончить игру", quit, 45)


        pygame.display.update()
        clock.tick(60)


def start_game():
    global score, make_jump, jump_count, player_y, health
    score = 0
    make_jump = False
    jump_count = 30
    player_y = display_h - player_h - 100
    health = 3

    while run_game():
        score = 0
        make_jump = False
        jump_count = 30
        player_y = display_h - player_h - 100
        health = 3



def run_game():
    global make_jump

    pygame.mixer_music.play(-1)

    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    stone, cloud = open_random_object()
    heart = Object(display_w, 280, 50, health_image, 4)

    button = Button(100, 50)

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
        print_text('Счёт: ' + str(score), 600, 10)


        move_objects(stone, cloud)
        draw_array(array)
        count_score(cactus_arr)

        heart.move()
        add_heart(heart)
        draw_dino()

        if check_collision(cactus_arr):
            game = False
            # pygame.mixer_music.stop()

        show_health()


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
            radius += 280
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)
    return radius



def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            object_return(array, cactus)


def object_return(objects, obj):
    radius = find_radius(objects)

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    obj.return_selfcactus(radius, height, width, img)

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

    pygame.mixer_music.pause()
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

    pygame.mixer_music.unpause()

def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 449:
            if not make_jump:
                if barrier.x <= player_x + player_w - 35 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True

            elif jump_count >= 0:
                if player_y + player_h - 5 >= barrier.y:
                    if barrier.x <= player_x + player_w - 40 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if player_y + player_h - 10 >= barrier.y:
                    if barrier.x <= player_x <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
        else:
            if not make_jump:
                if barrier.x <= player_x + player_w - 5 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_count == 10:
                if player_y + player_h - 5 >= barrier.y:
                    if barrier.x <= player_x + player_w - 5 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            elif jump_count >= -1:
                if player_y + player_h - 5 >= barrier.y:
                    if barrier.x <= player_x + player_w - 35 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if player_y + player_h - 10 >= barrier.y:
                    if barrier.x <= player_x + 5 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
    return False


def count_score(barriers):
    above_cactus = 0
    global score, max_above

    if -20 <= jump_count < 25:
        for barrier in barriers:
            if player_y + player_h - 5 <= barrier.y:
                if barrier.x <= player_x <= barrier.x + barrier.width:
                    above_cactus += 1
                elif barrier.x <= player_x + player_w <= barrier.x + barrier.width:
                    above_cactus += 1
        max_above = max(max_above, above_cactus)
    else:
        if jump_count == -30:
            score += max_above
            max_above = 0

def add_heart(heart):
    global health, player_x, player_y, player_w, player_h
    if player_x <= heart.x <= player_x + player_w:
        if player_y <= heart.y <= player_y + player_h:
            pygame.mixer.Sound.play(hp_sound)
            if health < 3:
                health += 1

            radius = display_w + random.randrange(500, 1700)
            heart.return_selfcactus(radius, heart.y, heart.width, heart.image)



def GameOver():
    global score, maxScore
    if score > maxScore:
        maxScore = score
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        restart_button = Button(200, 70)
        print_text('Нажмите на кнопку для выхода в меню:', 130, 200)
        restart_button.draw(300, 250, 'В меню', show_menu, 45)

        print_text('Рекорд: ' + str(maxScore), 350, 350)

        pygame.display.update()
        clock.tick(15)

show_menu()
pygame.quit()
quit()