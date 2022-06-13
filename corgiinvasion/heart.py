import pygame
from pygame.sprite import Sprite


class Hearts(Sprite):
    """A class to manage hearts for hit's limit of the Corgi."""
    def __init__(self, screen):
        super(Hearts, self).__init__()
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load('images/heart.bmp'), (20, 20))
        self.rect = self.image.get_rect()
