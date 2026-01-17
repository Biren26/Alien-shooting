import pygame
import random
import math

from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# create the background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Create the player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# create the enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# create the bullet
# ready - you can't see the bullet
# fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score of the player
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# position of Score
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


# function for creating score
def show_score(X, Y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (X, Y))


# function for creating Game over
def game_over_text():
    over_text = over_font.render('GAME OVER ', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# coll[sion detection btw bullet and enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


# blit function draw image of player  in screen
def player(X, Y):
    screen.blit(playerImg, (X, Y))


# blit function to draw image of enemy in screen
def enemy(X, Y, i):
    screen.blit(enemyImg[i], (X, Y))


# blit function to draw image of bullet
def fire_bullet(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (X + 16, Y + 10))


# Game loop/ hold the window
running = True
while running:
    # RGB- for background color
    screen.fill((0, 0, 0))

    # Create the image of background
    screen.blit(background, (0, 0))

    # allow to close the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keyStoke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # check if keyStoke is released or not
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # update player position
    playerX += playerX_change

    # It trapes the player inside the boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # provide movement of enemies
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # enemy movement
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # disappearing of enemy and bullet
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # function call for enemy
        enemy(enemyX[i], enemyY[i], i)

    # allow bullet to fire multiple time
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # function call for player
    player(playerX, playerY)

    # function call for score
    show_score(textX, textY)

    pygame.display.update()
