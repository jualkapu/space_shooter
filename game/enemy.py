import pygame

WIDTH, HEIGHT = 600, 800
enemy_radius = 30

# Load custom character image
enemy_image = pygame.image.load("enemy1.png")
# Resize the image to match the player's size
enemy_image = pygame.transform.scale(enemy_image, (enemy_radius * 2, enemy_radius * 2))

# Load custom character image
enemy_image2 = pygame.image.load("enemy2.png")
# Resize the image to match the player's size
enemy_image2 = pygame.transform.scale(enemy_image2, (enemy_radius * 2, enemy_radius * 2))

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.hit_box = pygame.Rect(x, y, enemy_radius * 2, enemy_radius * 2)  

    def move(self):
        self.y += self.speed
        self.hit_box.x = self.x
        self.hit_box.y = self.y

    def draw(self, screen):
        if self.speed == 1:
            screen.blit(enemy_image, (self.x, self.y))
        if self.speed == 2:
            screen.blit(enemy_image2, (self.x, self.y))
