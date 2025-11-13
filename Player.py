from enum import Enum, auto
import pygame
from settings import *


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
        self.original_surf =  pygame.Surface((PLAYER_SIZE)).convert_alpha()
        self.original_surf.fill('white')
        self.image = self.original_surf

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

        # Rotation
        # lerp needs:
        #  a - starting rotation point
        # b - finishing rotation point
        # t - where i am in the animation

        # state managment needs
        # rotating? - boolean

        # rotation function needs
        # how much to rotate each frame
        # direction
        # they are represented in the same variable
        # rotation = rotation speed (maybe 50) * dt
        self.starting_rotation = 0
        self.ending_rotation = 0
        self.t = 0
        self.rotation_state = False
        self.rotation = 0
        self.rotation_direction = 0
        self.rotation_duration = 0.25
        self.last_rotation_direction = self.rotation_direction

    def start_rotation(self, direction, target, duration):

        if not self.rotation_state:
            self.rotation_state = True
            self.starting_rotation = self.rotation
            self.ending_rotation = self.starting_rotation + target * direction
            self.t = 0
            self.rotation_duration = duration

    def update_rotation(self, dt):



        self.t += dt / self.rotation_duration

        if self.t>= 1:
            # if you finished rotation "snap to target"
            # means set all values to the finishing state to prevent errors
            self.t=1
            self.rotation = self.ending_rotation
            self.rotation_state = False
            self.image = pygame.transform.rotate(self.original_surf, self.rotation)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
 
            self.rotation = self.starting_rotation + (self.ending_rotation-self.starting_rotation) * self.t

            self.image = pygame.transform.rotate(self.original_surf, self.rotation)
            self.rect = self.image.get_rect(center = (self.rect.center))



    def movement(self,dt):

        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d])-int(keys[pygame.K_a])
        self.rotation_direction =  self.direction.x * -1
        if self.rotation_direction != 0: self.last_rotation_direction = self.rotation_direction
        if not self.rotation_state and self.direction.x != 0:
            self.start_rotation(self.rotation_direction, 90, 0.15)




        
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
        self.start_rotation(self.last_rotation_direction,180,0.25)



    def double_jump(self):

        if self.vertical_state==VerticalState.JUMPING and not self.passive_state==PassiveState.BOUNCED:

            if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                
                self.speedy -= (JUMPING_STRENGTH)
                self.previous_vertical_state = self.vertical_state
                self.vertical_state = VerticalState.DOUBLE_JUMP
            if self.previous_vertical_state==VerticalState.JUMPING and self.vertical_state==VerticalState.DOUBLE_JUMP:

                self.speedy= -1600
                self.gravity= 5500


    def update(self,dt):
        self.update_rotation(dt)
        self.movement(dt)
        self.double_jump()
        self.jump()
        self.apply_gravity(dt)
        self.collisions()




