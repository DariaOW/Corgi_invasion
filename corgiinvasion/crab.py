import pygame
from random import randint
from pygame.sprite import Sprite


class Crab(Sprite):
    def __init__(self, screen):
        Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load('images/crab.bmp'), (100, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.screen_rect = screen.get_rect()
        self.rect.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, stats):
        speed_x = randint(-1 - stats.crab_level, 1 + stats.crab_level)
        speed_y = randint(-1 - stats.crab_level, 1 + stats.crab_level)
        self.rect.left += speed_x
        self.rect.top += speed_y
        self.rect.clamp_ip(self.screen_rect)


def update_crabs(crabs, screen, stats):
    if crabs:
        crabs.update(stats)
    else:
        crab = Crab(screen)
        crabs.add(crab)
