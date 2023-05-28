import pygame
from random import randint
pygame.init()

# consts
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 1024
DINO_IMG = 'dino.png'
CACTUS_IMG = 'cactus.png'
BIRD_IMG = 'bird.png'
EARTH_IMG = 'earth.png'
# consts

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0, width=0, height=0):
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Dino(Sprite):
    def __init__(
        self, image, x=0, y=0, width=0, height=0,
        k_up=pygame.K_UP
    ):

        super().__init__(image, x, y, width, height)
        self.k_up = k_up





