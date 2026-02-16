import pygame
from settings import *
import random

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.image.load('./assets/tile.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2 +200))
