from enum import Enum, auto
import pygame
from settings import *
from PlayerState import PLAYER_STATE
from states import *
from Animation import Animation


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, platforms):
        super().__init__(groups)

        # image
        self.border_radius = 0
        self.original_surf = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.original_surf, PLAYER_COLOR, self.original_surf.get_rect(), border_radius=self.border_radius)
        self.image = self.original_surf
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT-PLATFORM_SIZE[1]))


        # interactions
        self.platforms = platforms

        # physics variables
        self.direction = pygame.Vector2(0,0)
        self.speedy = 450
        self.gravity = GRAVITY

        # Animations
        self.rotation = Animation('rotate', RotateState.ROTATING)
        self.movement_obj = Animation('horizontal',HorizontalState.MOVING_RIGHT if self.direction.x > 0 else HorizontalState.MOVING_LEFT)
        self.morph_circle = Animation('shape', ShapeState.MORPH_TO_CIRCLE)
        self.morph_square = Animation('shape', ShapeState.MORPH_TO_SQUARE)

    def morph(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_SPACE]:
            match PLAYER_STATE.shape:
                case  ShapeState.IDLE_SQUARE:
                    self.morph_circle.start_animation(1,0.5,int(PLAYER_SIZE[0]/2), 0)
                case ShapeState.IDLE_CIRCLE:
                    self.morph_square.start_animation(1,0.5,0,int(PLAYER_SIZE[0]/2))


    def movement(self):

        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT])-int(keys[pygame.K_a] or keys[pygame.K_LEFT])

        if PLAYER_STATE.horizontal == HorizontalState.IDLE and self.direction.x != 0:
            self.rotation.direction =  self.direction.x * -1
            self.rotation.start_animation(self.rotation.direction, MOVEMENT_SPEED, 90, 0)
            self.movement_obj.start_animation(self.direction.x, MOVEMENT_SPEED, PLAYER_SIZE[0], self.rect.centerx)

        
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
                self.gravity += 400
            self.speedy += self.gravity * dt
            self.rect.y += self.speedy * dt


    def jump(self):

        if pygame.key.get_just_pressed()[pygame.K_w]:
            if PLAYER_STATE.vertical==VerticalState.GROUNDED and PLAYER_STATE.bounce==BounceState.BOUNCED:
                self.speedy = - (JUMPING_STRENGTH)
                PLAYER_STATE.bounce = BounceState.DID_NOT_BOUNCE
                PLAYER_STATE.vertical=VerticalState.JUMPING
                

    def bounce(self):
        self.speedy = - (JUMPING_STRENGTH/2)
        PLAYER_STATE.bounce=BounceState.BOUNCED
        PLAYER_STATE.vertical=VerticalState.BOUNCING
        if self.rotation.direction != 0: self.rotation.last_direction = self.rotation.direction
        self.rotation.start_animation(self.rotation.last_direction, 0.25, 180, 0)


    def double_jump(self):
            if pygame.key.get_just_pressed()[pygame.K_w]:
                if PLAYER_STATE.vertical==VerticalState.JUMPING and PLAYER_STATE.bounce==BounceState.DID_NOT_BOUNCE and PLAYER_STATE.double_jump == DoubleJumpState.NO:
             
                        PLAYER_STATE.double_jump=DoubleJumpState.YES
                        self.speedy= -1600
                        self.gravity= 5500

    def update_animations(self, dt):
        if PLAYER_STATE.rotate == RotateState.ROTATING:
            self.rotation.lerp_value = self.rotation.update(dt, RotateState.IDLE)
            self.image = pygame.transform.rotate(self.original_surf, self.rotation.lerp_value)
            self.rect = self.image.get_rect(center=self.rect.center)

        if PLAYER_STATE.horizontal != HorizontalState.IDLE:
            self.rect.centerx = self.movement_obj.update(dt,HorizontalState.IDLE)

        if PLAYER_STATE.shape == ShapeState.MORPH_TO_CIRCLE:
            self.border_radius = int(self.morph_circle.update(dt, ShapeState.IDLE_CIRCLE))
            self.original_surf = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
            pygame.draw.rect(self.original_surf, PLAYER_COLOR, self.original_surf.get_rect(), border_radius=self.border_radius)
            self.image = pygame.transform.rotate(self.original_surf, self.rotation.lerp_value)

        if PLAYER_STATE.shape == ShapeState.MORPH_TO_SQUARE:
            print(f'{self.border_radius} a')
            self.border_radius = int(self.morph_square.update(dt, ShapeState.IDLE_SQUARE))
            print(f'{self.border_radius} b')
            self.original_surf = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
            pygame.draw.rect(self.original_surf, PLAYER_COLOR, self.original_surf.get_rect(), border_radius=self.border_radius)
            self.image = pygame.transform.rotate(self.original_surf, self.rotation.lerp_value)

                

    def update(self,dt):
        
        self.update_animations(dt)
        self.morph()
        self.movement()
        self.double_jump()
        self.jump()
        self.apply_gravity(dt)
        self.collisions()





