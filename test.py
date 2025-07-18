import pygame
import random
import math
from pygame import mixer

# initialise
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("images/abstract-space-background-with-nebula-stars.jpg")

# Background sound
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

# Title and Logo
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("images/rocket.png")
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6
for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load("images/flying.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(20)


# Ready -> You can't fire the bullet
# Fire -> the bullet is currently moving


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet
bulletImg = pygame.image.load("images/bullet.png")
bulletX = random.randint(0, 736)
bulletY = 480
bulletX_change = 0
bulletY_change = 1.2
# Ready -> You can't fire the bullet
# Fire -> the bullet is currently moving
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False


# Score

score_val = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


def showScore(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


over_font = pygame.font.Font("freesansbold.ttf", 64)


def get_game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Game Loop
running = True
while running:
    # Color of the Screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # CLose the window
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            running = False
        # Check if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Bullet Sound
                    bullet_sound = mixer.Sound("sounds/laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # Check for key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # adding player boundaries
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    # adding enemy movement
    for i in range(number_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            get_game_over()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("sounds/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
    
    #Define Bullet Management
    bullets = []
bullet_speed = 1.2

#Update Bullet Firing
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_SPACE:
        if bullet_state == "ready":
            bullet_sound = mixer.Sound("sounds/laser.wav")
            bullet_sound.play()
            bullets.append([playerX + 16, playerY + 10])  # Add new bullet

#Update Bullet Movement
for bullet in bullets[:]:  # Iterate over a copy of the list
    bullet[1] -= bullet_speed
    if bullet[1] <= 0:
        bullets.remove(bullet)
    fire_bullet(bullet[0], bullet[1])
    
    #Check Bullet Collision
    for bullet in bullets[:]:
     for i in range(number_of_enemies):
        collision = isCollision(enemyX[i], enemyY[i], bullet[0], bullet[1])
     if collision:
            explosion_sound = mixer.Sound("sounds/explosion.wav")
            explosion_sound.play()
            bullets.remove(bullet)
            score_val += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            
 #Restarting after game over
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r:  # Restart on 'R' key press
        running = True
        score_val = 0
        enemyX = [random.randint(0, 735) for _ in range(number_of_enemies)]
        enemyY = [random.randint(50, 150) for _ in range(number_of_enemies)]
        bullets.clear()

 #Player Health
    player_health = 3
health_font = pygame.font.Font("freesansbold.ttf", 32)

def show_health():
    health_text = health_font.render(f"Health: {player_health}", True, (255, 255, 255))
    screen.blit(health_text, (650, 10))

# Deduct health if an enemy reaches the bottom
if enemyY[i] > 440:
    player_health -= 1
    enemyY[i] = random.randint(50, 150)
    enemyX[i] = random.randint(0, 735)
    if player_health <= 0:
        get_game_over()
        running = False

#enemy bullet list
enemy_bullets = []
enemy_bullet_speed = 0.8

#random enemy firing
import time

last_shot_time = time.time()  # Track time for firing cooldown

def enemy_fire_bullet(x, y):
    enemy_bullets.append([x + 16, y + 10])  # Add new enemy bullet

import pygame
import random
import math
import time
from pygame import mixer

# Initialize
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("images/abstract-space-background-with-nebula-stars.jpg")

# Background sound
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

# Title and Logo
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("images/rocket.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6
for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load("images/flying.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(20)

# Bullet
bulletImg = pygame.image.load("images/bullet.png")
bullets = []  # List of active bullets
bullet_speed = 1.2

# Enemy Bullet
enemy_bullets = []  # List of active enemy bullets
enemy_bullet_speed = 0.8
last_enemy_shot_time = time.time()

# Fonts
font = pygame.font.Font("freesansbold.ttf", 32)
over_font = pygame.font.Font("freesansbold.ttf", 64)

# Variables
score_val = 0
player_health = 3


def show_score(x, y):
    score = font.render(f"Score: {score_val}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_health(x, y):
    health = font.render(f"Health: {player_health}", True, (255, 255, 255))
    screen.blit(health, (x, y))


def get_game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    bullets.append([x + 16, y + 10])


def enemy_fire_bullet(x, y):
    enemy_bullets.append([x + 16, y + 10])


def is_collision(obj1_x, obj1_y, obj2_x, obj2_y, threshold=27):
    distance = math.sqrt((obj1_x - obj2_x)**2 + (obj1_y - obj2_y)**2)
    return distance < threshold


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            if event.key == pygame.K_SPACE:
                fire_bullet(playerX, playerY)
            if event.key == pygame.K_r:  # Restart
                score_val = 0
                player_health = 3
                bullets.clear()
                enemy_bullets.clear()
                for i in range(number_of_enemies):
                    enemyX[i] = random.randint(0, 735)
                    enemyY[i] = random.randint(50, 150)
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                playerX_change = 0

    # Player Movement
    playerX += playerX_change
    playerX = max(0, min(736, playerX))  # Boundaries

    # Enemy Movement and Shooting
    for i in range(number_of_enemies):
        if enemyY[i] > 440:  # Enemy reaches the bottom
            player_health -= 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            if player_health <= 0:
                get_game_over()
                running = False
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        if time.time() - last_enemy_shot_time > 2:  # Enemy fires every 2 seconds
            enemy_fire_bullet(enemyX[i], enemyY[i])
            last_enemy_shot_time = time.time()

        collision = any(
            is_collision(enemyX[i], enemyY[i], bullet[0], bullet[1]) for bullet in bullets
        )
        if collision:
            score_val += 1
            bullets = [
                bullet for bullet in bullets if not is_collision(enemyX[i], enemyY[i], bullet[0], bullet[1])
            ]
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        screen.blit(bulletImg, (bullet[0], bullet[1]))

    # Enemy Bullet Movement
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet[1] += enemy_bullet_speed
        if enemy_bullet[1] > 600:
            enemy_bullets.remove(enemy_bullet)
        elif is_collision(playerX, playerY, enemy_bullet[0], enemy_bullet[1]):
            player_health -= 1
            enemy_bullets.remove(enemy_bullet)
            if player_health <= 0:
                get_game_over()
                running = False
        screen.blit(bulletImg, (enemy_bullet[0], enemy_bullet[1]))

    # Draw Player, Health, and Score
    player(playerX, playerY)
    show_score(10, 10)
    show_health(650, 10)

    pygame.display.update()




# Images source flaticon.com
