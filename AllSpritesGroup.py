import pygame

class AllSpritesGroup(pygame.sprite.Group):
    def draw(self,surface):
        for sprite in self:
            rect = getattr(sprite, "drawing_rect", sprite.rect)
            surface.blit(sprite.image,rect)