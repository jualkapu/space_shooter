from asyncio.windows_events import NULL
import pygame
import sys
import random
from game.player import Player
from game.bullet import Bullet
from game.star import Star
from game.enemy import Enemy
from game.start_menu import StartMenu

# Initialize Pygame
pygame.init()

# Define constant variables
ENEMY_SPAWN_INTERVAL = 1000 # Defines the interval which enemies spawn
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800 # Defines the size of the screen
BLACK = (0, 0, 0) # Colour black
NUM_STARS = 75 # Defines the number of start on the background
TARGET_FPS = 140  # Desired frame rate (e.g., 60 FPS)
PLAYER_RADIUS = 20
# Define game states
START = 0
PLAYING = 1
GAME_OVER = 2
current_state = START

# TODO: This could propably be get ridden of
ENEMY_RADIUS = 20 # Enemies radius that is used in the spawn location calculation

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Create a clock object to control the frame rate
clock = pygame.time.Clock()
# Create a list to store active enemies
active_enemies = []
# Create a list to store active bullets
bullets = []
# Initialize a variable to track the time of the last enemy spawn
last_enemy_spawn_time = 0
# Track if the spacebar is currently being pressed
space_pressed = False
# Track the time of the last shot taken by player
last_shot_time = 0
# Create a player
player = Player()
# Initialize stars for the backgroung of the game
stars = []
for _ in range(NUM_STARS):

    # Chooses random beginning coordinates for the stars
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    speed = random.random() # returns [0,1]
    stars.append(Star(x, y, speed))


# Handles all the drawing that is done on screenevery frame
def handleDrawing(bullets, stars, player, enemies):
    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)

    # Draw stars
    for star in stars:
        star.draw(screen)

    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)

    # Draw the player
    player.draw(screen)


# Updates the positions and blinking states of the stars. 
def handleStars(stars):
    for star in stars:
        # Increases the y coordinate by its speed, causing it to move downward.
        star.y += star.speed

        # If the star is not already blinking and a random number is less than the "BLINK_PROBABILITY"
        if not star.is_blinking and random.random() < star.blink_probability:
            star.is_blinking = True
            star.blink_duration = random.randint(*star.blink_duration_range)

        # If the star is already blinking, its "blink_duration" is reduced by 1 in each frame as the function is called once per frame
        if star.is_blinking:
            star.blink_duration -= 1

            # At 0, the blinking stops
            if star.blink_duration == 0:
                star.is_blinking = False

        # At the bottom, star is repositioned to the top of the screen with a new random x coordinate.
        if star.y > SCREEN_HEIGHT:
            star.x = random.randint(0, SCREEN_WIDTH)
            star.y = 0

    return stars


# Updates the positions of the bullets.
def handleBullets(bullets):
    active_bullets = []

    for bullet in bullets:

        # Updates the y coordinate of the bullet, causing it to move upwards.
        bullet.move()

        # If y coordinate is less than 0, it'soff the screen. Only bullets that are "on screen" need to be updated next frame.
        if bullet.y > 0:
            active_bullets.append(bullet)

    return active_bullets


# Updates enemy locations and spaw, return the latest enemy spawn time 
def handleEnemies(active_enemies, current_time, last_enemy_spawn_time):
    # Check if it's time to spawn a new enemy
    if current_time - last_enemy_spawn_time >= ENEMY_SPAWN_INTERVAL:
        spawn_enemy()
        # Update the last enemy spawn time
        last_enemy_spawn_time = current_time

    # Move active enemies downward
    for enemy in active_enemies:
        enemy.move()  

    # return the latest enemy spawn time 
    return last_enemy_spawn_time


# Creates new enemies on the random x coordinate on top of the screen, and adds them to list of active enemies
def spawn_enemy():
    # Random x-coordinate within the SCREEN_WIDTH
    x = random.randint(0, SCREEN_WIDTH - ENEMY_RADIUS * 2)  

    # Creates a new instance of "enemy" class
    enemy = Enemy(x, 0, random.randint(1,2))  

    # Adds new enemies to list of active enemies
    active_enemies.append(enemy)


# Handles the collisions of bullets and active enemies
def collisionHandler(bullets, active_enemies):
    # List to store the indexes of bullet and enemy pairs that have collided.
    collisions = []

    # The outer loop iterates through the bullets in the bullets list.
    for i, bullet in enumerate(bullets):
        bullet_rect = bullet.hit_box

        # Inner loop iterates through the active enemies in the active_enemies list.
        for j, enemy in enumerate(active_enemies):
            enemy_rect = enemy.hit_box

            # If the hitbox of a bullet collides with the hitbox of an enemy: bullet has hit the enemy.
            if bullet_rect.colliderect(enemy_rect):

                # Store the bullet and enemy that hit each other as a tuple
                collisions.append((i, j))    

    # Remove bullets that have collided with enemies. In reverse to avoid index errors when removing elements from the lists.
    for bullet_index, enemy_index in reversed(collisions):
        del bullets[bullet_index]
        del active_enemies[enemy_index]

    # Return bullets and active_enemies lists, where collided bullets and enemies have been removed.
    return bullets, active_enemies


# Handles players input for movement and shooting.
def handleInput(player, bullets, last_shot_time, space_pressed, current_time):
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
    if keys[pygame.K_SPACE] and current_time - last_shot_time >= player.shooting_cooldown * 1000 and not space_pressed:
        # Create a new bullet at the player's position
        bullet = Bullet(player.x + PLAYER_RADIUS, player.y)
        bullets.append(bullet)
        last_shot_time = current_time
        space_pressed = True
    elif not keys[pygame.K_SPACE]:
        space_pressed = False

    return bullets, last_shot_time, space_pressed


# Resets game back to starting state
def resetGame(active_enemies, bullets, player):
    active_enemies = []
    bullets = []
    player.moveToStart()
    return active_enemies, bullets


# Handles drawing of game over screen, tracks user input and changes the game state if game is restarted 
def game_over_screen():
    # Create a font for the game over message
    game_over_font = pygame.font.Font(None, 48)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)

    # Create a font for the restart and quit options
    options_font = pygame.font.Font(None, 36)
    restart_text = options_font.render("Play Again (Press SPACE)", True, (255, 255, 255))
    restart_rect = restart_text.get_rect()
    restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

    quit_text = options_font.render("Quit (Press Q)", True, (255, 255, 255))
    quit_rect = quit_text.get_rect()
    quit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)

    # Draw the game over message and options on the screen
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(quit_text, quit_rect)

    # Update the display
    pygame.display.flip()

    # Check for user input to restart or quit the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:               
                    return PLAYING
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# ------------------------------------------------------
#              MAIN GAME LOOP STARTS HERE
# ------------------------------------------------------

while True:

    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if current_state == START:
        # Draw the start menu "Press SPACE to Start"
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_state = PLAYING

    if current_state == GAME_OVER:
        active_enemies, bullets = resetGame(active_enemies, bullets, player)
        last_enemy_spawn_time, last_shot_time = current_time, current_time
        current_state = game_over_screen()

    bullets, last_shot_time, space_pressed = handleInput(player, bullets, last_shot_time, space_pressed, current_time)
    stars = handleStars(stars)
    bullets = handleBullets(bullets)
    # TODO: Enemy spawn time should be handled in a smarter way. This seems a bit iffy
    last_enemy_spawn_time = handleEnemies(active_enemies, current_time, last_enemy_spawn_time)
    bullets, active_enemies = collisionHandler(bullets, active_enemies)


    for enemy in active_enemies:
        if enemy.y > SCREEN_HEIGHT:
            current_state = GAME_OVER

    # Clear the screen
    screen.fill(BLACK)

    handleDrawing(bullets, stars, player, active_enemies)

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
