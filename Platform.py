import pygame
from settings import *
import random

class Platform(pygame.sprite.Sprite):
    def __init__(self, groups, pos, size):
        super().__init__(groups)

        self.image = pygame.Surface((size))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(midbottom = pos)

    def create_random_platforms( platforms_to_create, groups):
        platform_height = 200
        platform_width = 100
        gap = 00
        height_var = 0
        width_var = 0

        for i in range(1,platforms_to_create):

            
            gap +=150
            height_var+=random.choice((random.randint(50,100),random.randint(-150,-50)))
            width_var+=random.choice((random.randint(50,100),random.randint(-50,0)))
            height = max(1, platform_height+height_var)
            width = max(1, platform_width+width_var)

            Platform((groups),(100*i+gap,WINDOW_HEIGHT),(width,height))
