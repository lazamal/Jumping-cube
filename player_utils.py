from settings import *

def player_window_collisions(rect):
    if  rect.right >= WINDOW_WIDTH:
         rect.right = WINDOW_WIDTH

    if  rect.left <= 0:
         rect.left = 0

    if rect.top <=0:
         rect.top = 0
    