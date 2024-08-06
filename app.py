import pygame
import sys
import random
import time

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Enhanced Game')

# Устанавливаем цвета
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Создаем простые изображения
player_skin1 = pygame.Surface((50, 50))
player_skin1.fill(blue)
player_skin2 = pygame.Surface((50, 50))
player_skin2.fill(green)
enemy_skin1 = pygame.Surface((50, 50))
enemy_skin1.fill(red)
enemy_skin2 = pygame.Surface((50, 50))
enemy_skin2.fill(yellow)
laser_img = pygame.Surface((5, 20))
laser_img.fill(red)
background_img = pygame.Surface((screen_width, screen_height))
background_img.fill(black)

# Устанавливаем размеры изображений
player_size = player_skin1.get_width()
enemy_size = enemy_skin1.get_width()
laser_width = laser_img.get_width()
laser_height = laser_img.get_height()
boss_size = 100

# Устанавливаем параметры игрока
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - player_size - 10
player_speed = 5
player_skin = player_skin1

# Устанавливаем параметры лучей
laser_speed = 10
lasers = []
last_shot_time = 0
reload_time = 0.5  # Время перезарядки в секундах

# Устанавливаем параметры врагов
enemy_speed = 5
enemies = []
enemy_skins = [enemy_skin1, enemy_skin2]

# Устанавливаем параметры босса
boss = {'x': screen_width // 2 - boss_size // 2, 'y': 50, 'color': yellow, 'health': 100}

# Уровень сложности
difficulty_level = 1
start_time = time.time()
difficulty_interval = 5  # Интервал для увеличения сложности в секундах

def draw_player(x, y):
    screen.blit(player_skin, (x, y))

def draw_lasers(lasers):
    for laser in lasers:
        screen.blit(laser_img, (laser[0], laser[1]))

def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy[1], (enemy[0][0], enemy[0][1]))

def draw_boss(boss):
    pygame.draw.rect(screen, boss['color'], (boss['x'], boss['y'], boss_size, boss_size))

def move_lasers(lasers):
    for laser in lasers:
        laser[1] -= laser_speed
    return [laser for laser in lasers if laser[1] > 0]

def move_enemies(enemies):
    for i in range(len(enemies)):
        enemies[i][0][1] += enemy_speed + difficulty_level
    return [enemy for enemy in enemies if enemy[0][1] < screen_height]

def detect_collision(rect1, rect2):
    return (rect1[0] < rect2[0] + rect2[2] and
            rect1[0] + rect1[2] > rect2[0] and
            rect1[1] < rect2[1] + rect2[3] and
            rect1[1] + rect1[3] > rect2[1])

def game_over():
    pygame.quit()
    sys.exit()

def main():
    global player_x, player_y, lasers, enemies, difficulty_level, boss, player_skin, last_shot_time, start_time

    clock = pygame.time.Clock()
    enemy_spawn_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()

        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if keys[pygame.K_LEFT] or mouse_x < player_x:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or mouse_x > player_x + player_size:
            player_x += player_speed
        if mouse_pressed[0] and time.time() - last_shot_time > reload_time:
            lasers.append([player_x + player_size // 2 - laser_width // 2, player_y])
            last_shot_time = time.time()

        player_x = max(0, min(screen_width - player_size, player_x))

        # Move lasers
        lasers = move_lasers(lasers)

        # Spawn enemies
        enemy_spawn_time += 1
        if enemy_spawn_time > 20 - difficulty_level * 2:
            enemy_x = random.randint(0, screen_width - enemy_size)
            enemy_skin = random.choice(enemy_skins)
            enemies.append([[enemy_x, 0], enemy_skin])
            enemy_spawn_time = 0

        # Move enemies
        enemies = move_enemies(enemies)

        # Check for collisions
        player_rect = (player_x, player_y, player_size, player_size)
        for laser in lasers[:]:
            laser_rect = (laser[0], laser[1], laser_width, laser_height)
            for enemy in enemies[:]:
                enemy_rect = (enemy[0][0], enemy[0][1], enemy_size, enemy_size)
                if detect_collision(laser_rect, enemy_rect):
                    lasers.remove(laser)
                    enemies.remove(enemy)
                    break

        for enemy in enemies:
            if detect_collision(player_rect, (enemy[0][0], enemy[0][1], enemy_size, enemy_size)):
                game_over()

        # Clear screen and draw background
        screen.blit(background_img, (0, 0))

        # Draw everything
        draw_player(player_x, player_y)
        draw_lasers(lasers)
        draw_enemies(enemies)
        draw_boss(boss)

        # Update display
        pygame.display.flip()

        # Update difficulty level based on time
        current_time = time.time()
        if current_time - start_time > difficulty_interval and difficulty_level < 20:
            difficulty_level += 1
            start_time = current_time

        # Cap the frame rate
        clock.tick(30)

if __name__ == '__main__':
    main()
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
