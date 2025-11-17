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
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-PLATFORM_SIZE[1]))
        self.direction = pygame.Vector2(0,0)

        # interactions
        self.platforms = platforms

        # jump variables
        self.base_y_speed = 450
        self.speedy = self.base_y_speed
        self.previous_speedy = 0
        self.previous_y_pos = 0 
        self.gravity = GRAVITY


        # Rotation animation
        self.starting_rotation = 0
        self.ending_rotation = 0
        self.t = 0
        self.rotation = 0
        self.rotation_direction = 0
        self.rotation_duration = 0.25
        self.last_rotation_direction = self.rotation_direction

        self.rotation_animation = Animation('rotate', RotateState.ROTATING)
        self.rotation_animation.last_rotation_direction = 0


        # Movement Animation
        self.starting_movement = self.rect.centerx
        self.ending_movement = 0
        self.movement_t = 0
        self.movement_duration = 0.25



    def start_movement(self, direction, target, duration):
        if PLAYER_STATE.horizontal == HorizontalState.IDLE:
            PLAYER_STATE.horizontal = (
            HorizontalState.MOVING_RIGHT if direction > 0 else HorizontalState.MOVING_LEFT
        )
            self.starting_movement = self.rect.centerx
            self.ending_movement = self.starting_movement + target * direction
            self.movement_t = 0
            self.movement_duration = duration

    def update_movement(self,dt):
        if PLAYER_STATE.horizontal != HorizontalState.IDLE:
            self.movement_t += dt / self.movement_duration
            if self.movement_t >= 1:
                self.movement_t=1
                self.rect.centerx = self.ending_movement
                PLAYER_STATE.horizontal = HorizontalState.IDLE
            else:
                
                self.rect.centerx = lerp(self.starting_movement, self.ending_movement, self.movement_t)



    # def start_rotation(self, direction, target, duration):

    #     if PLAYER_STATE.rotate == RotateState.IDLE:
    #         PLAYER_STATE.rotate = RotateState.ROTATING
    #         self.starting_rotation = self.rotation
    #         self.ending_rotation = self.starting_rotation + target * direction
    #         self.t = 0
    #         self.rotation_duration = duration

    def update_rotation(self, dt):

        self.rotation_animation.t += dt / self.rotation_animation.duration

        if self.rotation_animation.t>= 1:
            # if you finished rotation "snap to target"
            # means set all values to the finishing state to prevent errors
            self.rotation_animation.t=1
            self.rotation_animation.lerp_value = self.rotation_animation.end
            PLAYER_STATE.rotate = RotateState.IDLE
            self.image = pygame.transform.rotate(self.original_surf, self.rotation_animation.lerp_value)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
 
            self.rotation_animation.lerp_value = lerp(self.rotation_animation.start, self.rotation_animation.end, self.rotation_animation.t)

            self.image = pygame.transform.rotate(self.original_surf, self.rotation_animation.lerp_value)
            self.rect = self.image.get_rect(center = (self.rect.center))

    def movement(self,dt):

        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d])-int(keys[pygame.K_a])
        self.rotation_direction =  self.direction.x * -1
        if self.rotation_direction != 0: self.last_rotation_direction = self.rotation_direction
        if PLAYER_STATE.rotate == RotateState.IDLE and self.direction.x != 0:
            self.rotation_animation.start_animation(self.direction.x * -1, MOVEMENT_SPEED, 90)
            # self.start_rotation(self.rotation_direction, 90, MOVEMENT_SPEED)
            self.start_movement(self.direction.x, PLAYER_SIZE[0], MOVEMENT_SPEED) 
        
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
        self.rotation_animation.start_animation(self.last_rotation_direction, 0.25, 180)
        # self.start_rotation(self.last_rotation_direction,180,0.25)

    def double_jump(self):
            if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                if PLAYER_STATE.vertical==VerticalState.JUMPING and PLAYER_STATE.bounce==BounceState.DID_NOT_BOUNCE and PLAYER_STATE.double_jump == DoubleJumpState.NO:
             
                        PLAYER_STATE.double_jump=DoubleJumpState.YES
                        self.speedy= -1600
                        self.gravity= 5500
                

    def update(self,dt):
        self.update_rotation(dt)
        self.update_movement(dt)
        self.movement(dt)
        self.double_jump()
        self.jump()

        self.apply_gravity(dt)
        self.collisions()





