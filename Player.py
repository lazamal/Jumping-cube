from enum import Enum, auto
import pygame
from easings_functions import easeInSine, easeOutSine
from settings import *
from PlayerState import PLAYER_STATE
from states import *
from Animation import Animation
from player_utils import *
import json

from utils import draw_circle, draw_morphing_square_circle


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, platforms):
        super().__init__(groups)

        # image
        self.border_radius = 0
        self.original_surf = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.original_surf, PLAYER_COLOR, self.original_surf.get_rect(), border_radius=self.border_radius)
        self.image = self.original_surf
        self.physics_rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-PLATFORM_SIZE[1]))
        self.drawing_rect = pygame.Rect.copy(self.physics_rect)
        
        # interactions
        
        self.platforms = platforms

        # physics variables
        self.direction = pygame.Vector2(0,0)
        self.speedy = 450
        self.gravity = GRAVITY

        # Animations
        self.rotation = Animation('rotate')
        self.movement_obj = Animation('horizontal')
        self.morph_circle = Animation('shape')
        self.morph_square = Animation('shape')


    def morph(self):
  
          if pygame.key.get_just_pressed()[pygame.K_LSHIFT]:
            match PLAYER_STATE.shape:
                case  ShapeState.IDLE_SQUARE:
                    self.morph_circle.start_animation(1,0.5,int(PLAYER_SIZE[0]/2), 0, ShapeState.MORPH_TO_CIRCLE)
                case ShapeState.IDLE_CIRCLE:
                    self.morph_square.start_animation(1,0.5,0,int(PLAYER_SIZE[0]/2), ShapeState.MORPH_TO_SQUARE)


    def movement(self):

        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT])-int(keys[pygame.K_a] or keys[pygame.K_LEFT])

        if PLAYER_STATE.horizontal == HorizontalState.IDLE and self.direction.x != 0:
            self.rotation.direction =  self.direction.x * -1
            self.rotation.start_animation(self.rotation.direction, MOVEMENT_SPEED, 90, 0, RotateState.ROTATING)
            self.movement_obj.start_animation(self.direction.x, MOVEMENT_SPEED, PLAYER_SIZE[0], self.physics_rect.centerx, HorizontalState.MOVING_RIGHT if self.direction.x > 0 else HorizontalState.MOVING_LEFT)

        
        # אם זה זז באלחסון תנרמל את המהירות
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
            
    def collisions(self):

        player_window_collisions(self.physics_rect)

        for platform in self.platforms:
            if self.physics_rect.colliderect(platform.rect):
                if self.direction.x != 0:
                    if PLAYER_STATE.horizontal == HorizontalState.MOVING_LEFT:
                        pass
                        # print("moving left")
                        # if self.direction.x < 0: self.rect.left = platform.rect.right
                    elif PLAYER_STATE.horizontal == HorizontalState.MOVING_RIGHT:
                        pass
                         
                self.physics_rect.bottom = platform.rect.top
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
            self.physics_rect.y += self.speedy * dt


    def jump(self):

        if pygame.key.get_just_pressed()[pygame.K_w] or pygame.key.get_just_pressed()[pygame.K_UP] :
            if PLAYER_STATE.vertical==VerticalState.GROUNDED and PLAYER_STATE.bounce==BounceState.BOUNCED:
                self.speedy = - (JUMPING_STRENGTH)
                PLAYER_STATE.bounce = BounceState.DID_NOT_BOUNCE
                PLAYER_STATE.vertical=VerticalState.JUMPING
    

    def bounce(self):
        self.speedy = - (JUMPING_STRENGTH/2)
        PLAYER_STATE.bounce=BounceState.BOUNCED
        PLAYER_STATE.vertical=VerticalState.BOUNCING
        if self.rotation.direction != 0: self.rotation.last_direction = self.rotation.direction
        self.rotation.start_animation(self.rotation.last_direction, 0.25, 180, 0, RotateState.ROTATING)


    def double_jump(self):
            if pygame.key.get_just_pressed()[pygame.K_w] or pygame.key.get_just_pressed()[pygame.K_UP]:
                if PLAYER_STATE.vertical==VerticalState.JUMPING and PLAYER_STATE.bounce==BounceState.DID_NOT_BOUNCE and PLAYER_STATE.double_jump == DoubleJumpState.NO:
                        PLAYER_STATE.double_jump=DoubleJumpState.YES
                        self.speedy= -1600
                        self.gravity= 5500
                        

    def update_animations(self, dt):
        if PLAYER_STATE.rotate == RotateState.ROTATING:
            self.rotation.lerp_value = self.rotation.update(dt, RotateState.IDLE)
            self.image = pygame.transform.rotate(self.original_surf, self.rotation.lerp_value)
            self.physics_rect = self.image.get_rect(center=self.physics_rect.center)
            
        if PLAYER_STATE.horizontal != HorizontalState.IDLE:

            self.physics_rect.centerx = self.movement_obj.update(dt,HorizontalState.IDLE)

        if PLAYER_STATE.shape == ShapeState.MORPH_TO_CIRCLE:
            self.border_radius = int(self.morph_circle.update(dt, ShapeState.IDLE_CIRCLE,easing=easeOutSine ))
            self.image = draw_morphing_square_circle(self.border_radius, self.rotation.lerp_value)

        if PLAYER_STATE.shape == ShapeState.MORPH_TO_SQUARE:
            self.border_radius = int(self.morph_square.update(dt, ShapeState.IDLE_SQUARE, easing=easeInSine))
            self.image = draw_morphing_square_circle(self.border_radius, self.rotation.lerp_value)

        if PLAYER_STATE.shape == ShapeState.IDLE_CIRCLE:
                self.image = draw_circle()
                self.physics_rect = self.original_surf.get_rect(center=self.physics_rect.center)

    def sync_drawing_rect(self):
        self.drawing_rect = self.image.get_rect(center = self.physics_rect.center)

    def update(self,dt):
        self.morph()
        self.movement()
        self.double_jump()
        self.jump()
        self.apply_gravity(dt)
        self.update_animations(dt)
        self.collisions()
        self.sync_drawing_rect()
        PLAYER_STATE_asJson = json.dumps(dict([[item[0],item[2]] for item in (PLAYER_STATE)]))




