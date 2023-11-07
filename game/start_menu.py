import pygame

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.start_text = self.font.render("Press SPACE to Start", True, (255, 255, 255))
        self.start_text_rect = self.start_text.get_rect(center=screen.get_rect().center)

    def display(self):
        self.screen.blit(self.start_text, self.start_text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        return False
