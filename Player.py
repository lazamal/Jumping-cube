import pygame
from settings import *



class Player(pygame.sprite.Sprite):
    def __init__(self, groups, platforms):
        super().__init__(groups)

        self.image = pygame.Surface((PLAYER_SIZE))
        self.image.fill('white')
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-PLATFORM_SIZE[1]))
 
        self.speedx = 500
        self.speedy = 450
        self.direction = pygame.Vector2(0,0)
        self.is_jumping = False
        self.on_ground = True
        self.gravity = GRAVITY
        self.platforms = platforms

    def jump(self):
        if self.on_ground and not self.is_jumping:
            self.speedy = - (JUMPING_STRENGTH)
            self.is_jumping = True
            self.on_ground = False



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
                self.is_jumping=False
                self.on_ground = True
                self.gravity = GRAVITY

    def apply_gravity(self,dt):

            if not self.on_ground:
                self.speedy += self.gravity * dt
                self.gravity += 400
                if self.speedy >=10000:
                    self.speedy = 10000
            self.rect.y += self.speedy * dt
            

    def update(self,dt):
        self.apply_gravity(dt)
        self.movement(dt)
        self.collisions()

