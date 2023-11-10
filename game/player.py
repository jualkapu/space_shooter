import pygame

WIDTH, HEIGHT = 600, 800

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.speed = 3
        self.radius = 20
        self.shooting_cooldown = 0.5
        self.hit_box = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

        # Note: This way of loading the image is only acceptable when there is only one instance of this calss on the screen.
        # If there were multiple instances, the image would have to be loaded multiple times which takes time.
        # For example, in Enemies class this way of loading images was enough to make game unplayably slow.
        self.image = pygame.transform.scale(pygame.image.load("alus.png"), (self.radius * 2, self.radius* 2))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.hit_box.x = self.x
        self.hit_box.y = self.y

        if self.x < 0:
            self.x = 0
        if self.x > (WIDTH - self.radius*2):
            self.x = WIDTH - self.radius*2
        if self.y > (HEIGHT - self.radius*2):
            self.y = HEIGHT - self.radius*2
        if self.y < 100:
            self.y = 100

    def moveToStart(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))