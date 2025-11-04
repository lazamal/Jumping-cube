import pygame
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)

        self.image = pygame.Surface((PLATFORM_SIZE))
        self.image.fill('brown')
        self.rect = self.image.get_rect(midbottom = pos)