import pygame

class Cow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_idle = pygame.image.load("../assets/sprites/white_cow_idle.png")
        self.image_walk = pygame.image.load("../assets/sprites/white_cow_walk.png")

        self.rect = self.image_idle.get_rect()
        self.rect.x, self.rect.y = 100, 100
        self.speed = 5
        self.direction = "right"