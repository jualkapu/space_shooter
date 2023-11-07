import pygame

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class Star:
    def __init__(self, x, y, speed):
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.speed = speed # Determines how fast star moves down on screen
        self.radius = 1
        self.is_blinking = False
        self.blink_duration = 0
        self.blink_probability = 0.01
        self.blink_duration_range = (30, 60)


    def draw(self, screen):
        if self.is_blinking:
            pygame.draw.circle(screen, GRAY, (self.x, self.y), self.radius)
        else:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
