import pygame
import sys
import random
from game.player import Player
from game.bullet import Bullet
from game.star import Star
from game.enemy import Enemy

# Initialize Pygame
pygame.init()

# Define constant variables
ENEMY_SPAWN_INTERVAL = 1000
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
BLACK = (0, 0, 0)
ENEMY_RADIUS = 20
NUM_STARS = 75
TARGET_FPS = 140  # Desired frame rate (e.g., 60 FPS)
PLAYER_RADIUS = 20

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Create a clock object to control the frame rate
clock = pygame.time.Clock()

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

# Initialize stars
# Each entry in "stars" consist of x coordinate, y coordinate and speed value.
stars = []
for _ in range(NUM_STARS):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    speed = random.random()
    stars.append(Star(x, y, speed))

# Create a list to store active enemies
enemies = []
# Create a list to store active bullets
bullets = []
# Initialize a variable to track the time of the last enemy spawn
last_enemy_spawn_time = 0
# Track if the spacebar is currently being pressed
space_pressed = False
# Track the time of the last shot taken by player
last_shot_time = 0
# Add a shooting cooldown in seconds 
shoot_cooldown = 0.5

# This function handles all the drawing that is done on every frame
def drawingHandler(bullets, stars, player, enemies):
    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)
    # Draw stars
    for star in stars:
        star.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    # Draw the player
    player.draw(screen)

def handleStars(stars):
    # Update star positions and adjust speed based on player's vertical movement
    for star in stars:
        star.y += star.speed
        if star.y > SCREEN_HEIGHT:
            # Reset star when it goes off the screen
            star.x = random.randint(0, SCREEN_WIDTH)
            star.y = 0
    return stars

def handleBullets(bullets):
    new_bullets = []
    for bullet in bullets:
        bullet.move()
        if bullet.y > 0:
            new_bullets.append(bullet)
    return new_bullets
    
# Function to spawn a new enemy
def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH - ENEMY_RADIUS * 2)  # Random x-coordinate within the  SCREEN_WIDTH
    enemy = Enemy(x, 0, random.randint(1,2))  # Start enemies at the top of the screen
    enemies.append(enemy)

def collisionHandler(bullets, enemies):
    collisions = []
    for i, bullet in enumerate(bullets):
        bullet_rect = bullet.hit_box
        for j, enemy in enumerate(enemies):
            enemy_rect = enemy.hit_box
            if bullet_rect.colliderect(enemy_rect):
                collisions.append((i, j))  # Store the indices of bullet and enemy pairs   
    # Remove bullets that have collided with enemies
    for bullet_index, enemy_index in reversed(collisions):
        del bullets[bullet_index]
        del enemies[enemy_index]
    return bullets, enemies

# ------------------------------------------------------
#              MAIN GAME LOOP STARTS HERE
# ------------------------------------------------------
running = True
while running:

    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement using the Player class's move method
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move(-player.speed, 0)  # Move left
    if keys[pygame.K_d]:
        player.move(player.speed, 0)   # Move right
    if keys[pygame.K_w]:
        player.move(0, -player.speed)  # Move up
    if keys[pygame.K_s]:
        player.move(0, player.speed)   # Move down

     # Check if the spacebar is pressed and if it wasn't pressed in the previous frame
    if keys[pygame.K_SPACE] and current_time - last_shot_time >= shoot_cooldown * 1000 and not space_pressed:
        # Create a new bullet at the player's position
        bullet = Bullet(player.x + PLAYER_RADIUS, player.y)
        bullets.append(bullet)
        last_shot_time = current_time
        space_pressed = True
    elif not keys[pygame.K_SPACE]:
        space_pressed = False

    stars = handleStars(stars)
    bullets = handleBullets(bullets)
    bullets, enemies = collisionHandler(bullets, enemies)

    # Check if it's time to spawn a new enemy
    if current_time - last_enemy_spawn_time >= ENEMY_SPAWN_INTERVAL:
        spawn_enemy()  # Spawn a new enemy
        last_enemy_spawn_time = current_time  # Update the last enemy spawn time

    # Move enemies
    for enemy in enemies:
        enemy.move()  # Move enemies downward

    # Clear the screen
    screen.fill(BLACK)

    drawingHandler(bullets, stars, player, enemies)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(TARGET_FPS)

# ------------------------------------------------------
#               MAIN GAME LOOP ENDS HERE
# ------------------------------------------------------

# Quit Pygame and the program
pygame.quit()
sys.exit()
