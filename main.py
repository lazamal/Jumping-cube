import pygame
from settings import *
from Player import Player
from Platform import Platform
import random



class Game():
    def __init__(self):
        
        pygame.init()
        pygame.display.set_caption('Jumping Cube')
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True


        # group

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        # sprites

        # Platform.create_random_platforms(6, (self.all_sprites,self.platforms))
        self.platform = Platform((self.all_sprites,self.platforms),(WINDOW_WIDTH/2,WINDOW_HEIGHT), PLATFORM_SIZE )
        self.player = Player(self.all_sprites, self.platforms)


    def run(self):

        while self.running:
            dt =  self.clock.tick(60) / 1000



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            self.all_sprites.draw(self.screen)
            self.all_sprites.update(dt)

            pygame.display.flip()


        pygame.quit()

if __name__ == '__main__':
    game=Game()
    game.run()
