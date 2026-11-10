import pygame

class AllSpritesGroup(pygame.sprite.Group):
    def draw(self,surface):
        for sprite in self:
            rect = getattr(sprite, "drawing_rect", sprite.rect)
            surface.blit(sprite.image,rect)
            if hasattr(sprite, "drawing_rect"):
                pygame.draw.rect(surface, "red", sprite.rect, 1)
                # pygame.draw.rect(surface, "blue", sprite.drawing_rect, 1)