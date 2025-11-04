import pygame
from settings import *

class Floor(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.Surface((FLOOR_SIZE))
        self.image.fill('brown')
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT))