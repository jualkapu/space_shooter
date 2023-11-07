import pygame

WIDTH, HEIGHT = 600, 800
enemy_radius = 30

# Load custom character image
enemy_image = pygame.image.load("vihu.png")
# Resize the image to match the player's size
enemy_image = pygame.transform.scale(enemy_image, (enemy_radius * 2, enemy_radius * 2))

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
        screen.blit(enemy_image, (self.x, self.y))