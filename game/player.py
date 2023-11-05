import pygame

WIDTH, HEIGHT = 600, 800
player_x = WIDTH // 2
player_y = HEIGHT - 50
player_radius = 20

# Load custom character image
player_image = pygame.image.load("alus.png")
# Resize the image to match the player's size
player_image = pygame.transform.scale(player_image, (player_radius * 2, player_radius * 2))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        if self.x < 0:
            self.x = 0
        if self.x > (WIDTH - player_radius*2):
            self.x = WIDTH - player_radius*2
        if self.y > (HEIGHT - player_radius*2):
            self.y = HEIGHT - player_radius*2
        if self.y < 100:
            self.y = 100

    def draw(self, screen):
        screen.blit(player_image, (self.x, self.y))