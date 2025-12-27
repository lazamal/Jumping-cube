import pygame
from settings import *
import math
from easings_functions import *

def lerp(a, b, t, easing):
    return a + (b - a) * easing(t)


def draw_circle():

    # setup circle
    surface = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
    w, h = PLAYER_SIZE
    radius = min(w, h) // 2
    center = (w // 2, h // 2)

    # draw the circle
    pygame.draw.circle(surface, PLAYER_COLOR, center, radius)

    # return the surface to the image drawn
    return surface

def draw_morphing_square_circle(border_radius, rotation):

        surface = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)

        pygame.draw.rect(surface, PLAYER_COLOR, surface.get_rect(), border_radius=border_radius)
        image = pygame.transform.rotate(surface, rotation)
        return image
 
