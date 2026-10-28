import pygame
from Player import Player
from Platform import Platform
from settings import *
import pytest

# שאלות למחר
# למה אני צריך ליצור את האובייקטים לבדיקה בתוך הפונקציה ולא ברמת הקובץ?

@pytest.fixture
def platform_group():
    platform = pygame.sprite.Group()
    # return platform

@pytest.fixture
def all_sprites_group():
    all_sprites = pygame.sprite.Group()
    return all_sprites

@pytest.fixture
def player(all_sprites_group, platform_group):
    

    player = Player(all_sprites_group, platform_group)
    return player

@pytest.fixture
def platform(all_sprites_group, platform_group):

    platform = Platform((all_sprites_group, platform_group),(WINDOW_WIDTH/2,WINDOW_HEIGHT), PLATFORM_SIZE )
    return platform

def test_right_collision(player):

    player.rect.right = WINDOW_WIDTH + 1
    player.collisions()
    assert player.rect.right == WINDOW_WIDTH

def test_left_collision(player):

    player.rect.left = -1
    player.collisions()
    assert player.rect.left == 0

def test_player_platform_collision(player,platform_group, platform):
    player.rect.midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT)
    platform_collisions = pygame.sprite.spritecollide(player, platform_group, False)
    assert len(platform_collisions) != 0

def test_doesnt_fall_through_floor(player,platform, platform_group):
    player.rect.midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT)
    player.collisions()
    assert player.rect.bottom == platform.rect.top
    


        