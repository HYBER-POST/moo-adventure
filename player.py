import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/player.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)