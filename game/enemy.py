import pygame

WIDTH, HEIGHT = 600, 800
vihu_x = WIDTH // 2
vihu_y = 50
vihu_radius = 30

# Load custom character image
vihu_image = pygame.image.load("vihu.png")
# Resize the image to match the player's size
vihu_image = pygame.transform.scale(vihu_image, (vihu_radius * 2, vihu_radius * 2))

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.hit_box = pygame.Rect(x, y, vihu_radius * 2, vihu_radius * 2)  


    def move(self):
        self.y += self.speed
        self.hit_box.x = self.x
        self.hit_box.y = self.y

    def draw(self, screen):
        screen.blit(vihu_image, (self.x, self.y))