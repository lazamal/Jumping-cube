from enum import Enum, auto
import pygame
from settings import *
from utils import lerp
from PlayerState import PLAYER_STATE
from states import *
from Animation import Animation


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, platforms):
        super().__init__(groups)

        self.original_surf =  pygame.Surface((PLAYER_SIZE)).convert_alpha()
        self.original_surf.fill('white')
        self.image = self.original_surf
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT-PLATFORM_SIZE[1]))
        self.direction = pygame.Vector2(0,0)

        # interactions
        self.platforms = platforms

        # jump variables
        self.base_y_speed = 450
        self.speedy = self.base_y_speed
        self.previous_speedy = 0
        self.previous_y_pos = 0 
        self.gravity = GRAVITY


        self.rotation = Animation('rotate', RotateState.ROTATING)
        self.movement_obj = Animation('horizontal',HorizontalState.MOVING_RIGHT if self.direction.x > 0 else HorizontalState.MOVING_LEFT)
        

        

    def movement(self,dt):

        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d])-int(keys[pygame.K_a])

        if PLAYER_STATE.horizontal == HorizontalState.IDLE and self.direction.x != 0:
            self.rotation.direction =  self.direction.x * -1
            self.rotation.start_animation(self.rotation.direction, MOVEMENT_SPEED, 90, 0)
            self.movement_obj.start_animation(self.direction.x, MOVEMENT_SPEED, PLAYER_SIZE[0], self.rect.centerx)
        if self.rotation.direction != 0: self.rotation.last_direction = self.rotation.direction
        
        # אם זה זז באלחסון תנרמל את המהירות
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
            
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
                if not PLAYER_STATE.bounce==BounceState.BOUNCED:
                    self.bounce()
                else:
                    self.previous_vertical_state = PLAYER_STATE.vertical
                    PLAYER_STATE.vertical = VerticalState.GROUNDED
                    PLAYER_STATE.double_jump = DoubleJumpState.NO

 
    def apply_gravity(self,dt):
            
            if not PLAYER_STATE.vertical==VerticalState.GROUNDED:
                self.previous_speedy = self.speedy
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
            if PLAYER_STATE.vertical==VerticalState.GROUNDED and PLAYER_STATE.bounce==BounceState.BOUNCED:
                self.previous_speedy = self.speedy
                self.speedy = - (JUMPING_STRENGTH)

                PLAYER_STATE.bounce = BounceState.DID_NOT_BOUNCE
                self.previous_vertical_state = PLAYER_STATE.vertical
                PLAYER_STATE.vertical=VerticalState.JUMPING
                

    def bounce(self):
        self.previous_speedy = self.speedy
        self.speedy = - (JUMPING_STRENGTH/2)
        PLAYER_STATE.bounce=BounceState.BOUNCED
        self.previous_vertical_state = PLAYER_STATE.vertical
        PLAYER_STATE.vertical=VerticalState.BOUNCING
        self.rotation.start_animation(self.rotation.last_direction, 0.25, 180, 0)


    def double_jump(self):
            if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                if PLAYER_STATE.vertical==VerticalState.JUMPING and PLAYER_STATE.bounce==BounceState.DID_NOT_BOUNCE and PLAYER_STATE.double_jump == DoubleJumpState.NO:
             
                        PLAYER_STATE.double_jump=DoubleJumpState.YES
                        self.speedy= -1600
                        self.gravity= 5500

    def update_animation(self, dt):
        if PLAYER_STATE.rotate == RotateState.ROTATING:
            self.rotation.lerp_value = self.rotation.update(dt, RotateState.IDLE)
            self.image = pygame.transform.rotate(self.original_surf, self.rotation.lerp_value)
            self.rect = self.image.get_rect(center=self.rect.center)

        if PLAYER_STATE.horizontal != HorizontalState.IDLE:
            self.rect.centerx = self.movement_obj.update(dt,HorizontalState.IDLE)
                

    def update(self,dt):
        self.update_animation(dt)
        self.movement(dt)
        self.double_jump()
        self.jump()
        self.apply_gravity(dt)
        self.collisions()





