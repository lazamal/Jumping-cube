from enum import Enum, auto
import pygame
from settings import *


class PlayerState(Enum):
    IDLE = auto()
    MOVING_RIGHT = auto()
    MOVING_LEFT = auto()
    JUMPING=auto()
    FALLING=auto()
    BOUNCING=auto()

class HorizontalState(Enum):
    IDLE = auto()
    MOVING_LEFT = auto()
    MOVING_RIGHT = auto()

class VerticalState(Enum):
    JUMPING=auto()
    FALLING=auto()
    BOUNCING=auto()
    GROUNDED=auto()
    DOUBLE_JUMP = auto()

class PassiveState(Enum):
    BOUNCED= auto()
    DID_NOT_BOUNCE= auto()




class Player(pygame.sprite.Sprite):
    def __init__(self, groups, platforms):
        super().__init__(groups)

        self.image = pygame.Surface((PLAYER_SIZE))
        self.image.fill('white')
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-PLATFORM_SIZE[1]))

        self.base_y_speed = 450
        self.speedx = 500

        self.speedy = self.base_y_speed

        self.previous_speedy = 0
        self.previous_y_pos = 0 
        self.direction = pygame.Vector2(0,0)
        self.gravity = GRAVITY
        self.platforms = platforms

        # player states

        self.horizontal_state=HorizontalState.IDLE
        self.vertical_state=VerticalState.GROUNDED
        self.passive_state = PassiveState.BOUNCED
        self.previous_vertical_state = VerticalState.GROUNDED

                  

    def identify_states(self):
        
        if self.direction.x> 0:
            self.horizontal_state=HorizontalState.MOVING_RIGHT
        elif self.direction.x<0:
            self.horizontal_state=HorizontalState.MOVING_LEFT
        else:
            self.horizontal_state=HorizontalState.IDLE

        if self.speedy<0:
            self.previous_vertical_state = self.vertical_state
            self.vertical_state=VerticalState.JUMPING

        if self.passive_state == PassiveState.BOUNCED and self.speedy<0:
            self.previous_vertical_state = self.vertical_state
            self.vertical_state=VerticalState.BOUNCING

        # elif self.previous_y_pos<self.rect.y:
        #     self.previous_vertical_state = self.vertical_state
        #     self.vertical_state=VerticalState.FALLING

  

    def movement(self,dt):

        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d])-int(keys[pygame.K_a])
        
        # אם זה זז באלחסון תנרמל את המהירות
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        self.rect.centerx += self.direction.x * self.speedx * dt



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
                self.previous_speedy = self.speedy
                self.speedy = 0
                self.gravity = GRAVITY
                if not self.passive_state==PassiveState.BOUNCED:
                    self.bounce()
                else:
                    self.previous_vertical_state = self.vertical_state
                    self.vertical_state = VerticalState.GROUNDED
 


    def apply_gravity(self,dt):
            

            if not self.vertical_state==VerticalState.GROUNDED:
                self.previous_speedy = self.speedy
                # self.speedy += self.gravity * dt
                self.gravity += 400
                
                if self.speedy >=10000:
                    self.speedy = 10000
                if self.gravity >=10000:
                    self.gravity=10000


            self.speedy += self.gravity * dt

            movement = self.speedy * dt
            self.previous_y_pos= self.rect.y
            self.rect.y += movement
           

    def jump(self):

        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            if self.vertical_state==VerticalState.GROUNDED and self.passive_state==PassiveState.BOUNCED:
                self.previous_speedy = self.speedy
                self.speedy = - (JUMPING_STRENGTH)

                self.passive_state=PassiveState.DID_NOT_BOUNCE
                self.previous_vertical_state = self.vertical_state
                self.vertical_state=VerticalState.JUMPING



    def bounce(self):
        self.previous_speedy = self.speedy
        self.speedy = - (JUMPING_STRENGTH/2)
        self.passive_state=PassiveState.BOUNCED
        self.previous_vertical_state = self.vertical_state
        self.vertical_state=VerticalState.BOUNCING



    def double_jump(self):

        if self.vertical_state==VerticalState.JUMPING and not self.passive_state==PassiveState.BOUNCED:

            if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                
                self.speedy -= (JUMPING_STRENGTH)
                self.previous_vertical_state = self.vertical_state
                self.vertical_state = VerticalState.DOUBLE_JUMP
            if self.previous_vertical_state==VerticalState.JUMPING and self.vertical_state==VerticalState.DOUBLE_JUMP:
                print('found the moment')
                self.speedy=-1800
                self.gravity=5500
                print(self.speedy)
                print(self.gravity)

    def update(self,dt):
        # self.identify_states()
        # print(f'horizontal state is{self.horizontal_state}')
        # print(f'vertical state is{self.vertical_state}')
        # print(f'passive state is{self.passive_state}')


        self.movement(dt)
        self.double_jump()
        self.jump()

        self.apply_gravity(dt)
        self.collisions()
        



