import pygame
GREEN = (51, 255, 51)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4  
        self.hit_box = pygame.Rect(x - 2.5, y, 5, 20)

    def move(self):
        self.y -= self.speed
        self.hit_box.y = self.y

    def draw(self, screen):
        bullet_width = 5  # Adjust the width of the bullet rectangle
        bullet_height = 20  # Adjust the height of the bullet rectangle
        bullet_color = GREEN  # Adjust the bullet color as needed

        bullet_rect = pygame.Rect(self.x - bullet_width // 2, self.y, bullet_width, bullet_height)
        pygame.draw.rect(screen, bullet_color, bullet_rect)