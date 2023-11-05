import pygame

WHITE = (255, 255, 255)
STAR_RADIUS = 1

class Star:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), STAR_RADIUS)