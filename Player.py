from enum import Enum, auto
import pygame
from settings import *


class PlayerState(Enum):
    IDLE = auto()
    MOVING = auto()
    JUMPING=auto()
    LANDING=auto()
    BOUNCING=auto()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, platforms):
        super().__init__(groups)

        self.image = pygame.Surface((PLAYER_SIZE))
        self.image.fill('white')
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-PLATFORM_SIZE[1]))
 
        self.speedx = 500
        self.speedy = 450
        self.direction = pygame.Vector2(0,0)
        self.gravity = GRAVITY
        self.platforms = platforms

        # player states
        self.is_jumping = False
        self.on_ground = True
        self.bounced = True

        self.player_state = PlayerState.IDLE

 

    def manage_states(self, state):
        if state == 'has not jumped yet':
            self.on_ground = True
            self.is_jumping=False
            self.bounced = True
        elif state == 'jumping':
            self.is_jumping = True
            self.on_ground = False
            self.bounced=False    
        elif state == 'bouncing':
            self.bounced = True
            self.is_jumping=False
            self.on_ground = False
        else:
            print('no such state')

    



    def movement(self,dt):

        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d])-int(keys[pygame.K_a]) 

        # אם זה זז באלחסון תנרמל את המהירות
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        self.rect.centerx += self.direction.x * self.speedx * dt

        if keys[pygame.K_SPACE]:
            self.jump()


    def collisions(self):

        if self.rect.right >= WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.top <=0:
            self.rect.top = 0


        platform_collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        if platform_collisions:

            for platform in platform_collisions:
                self.rect.bottom = platform.rect.top
                self.speedy = 0
                self.gravity = GRAVITY
                if not self.bounced:
                    self.bounce()
                else:
                    self.manage_states('has not jumped yet')
  

        else:
            self.on_ground = False




    def apply_gravity(self,dt):

            if not self.on_ground:
                self.speedy += self.gravity * dt
                self.gravity += 400

                if self.speedy >=10000:
                    self.speedy = 10000
            movement = self.speedy * dt

            self.rect.y += movement


            

    def jump(self):
        
        if self.on_ground and not self.is_jumping and self.bounced:
            self.speedy = - (JUMPING_STRENGTH)
            self.manage_states('jumping')

    def bounce(self):
        self.speedy = - (JUMPING_STRENGTH/2)
        self.manage_states('bouncing')
        

    def update(self,dt):
        self.movement(dt)
        self.apply_gravity(dt)
        self.collisions()
        



