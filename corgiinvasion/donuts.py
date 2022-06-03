import random
import pygame
from pygame.sprite import Sprite


class Donut(Sprite):
    def __init__(self, screen):
        super(Donut, self).__init__()
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(random.choice(['images/donut1.bmp', 'images/donut2.bmp',
                                                                             'images/donut3.bmp'])), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed_factor = 0.2

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, stats, height):
        self.y += self.speed_factor + stats.donut_speed_level
        self.rect.y = self.y
        if self.rect.y > height:
            self.kill()


def create_donuts(screen, donuts, donut_number):
    donut = Donut(screen)
    donut_width = donut.rect.width
    donut.x = donut_width + 2 * donut_width * donut_number
    donut.rect.x = donut.x
    donut.rect.y = donut.rect.height + 2 * donut.rect.height
    donuts.add(donut)


def get_number_donuts_x(width, donut_width):
    available_space_x = width - 2 * donut_width
    number_donuts_x = int(available_space_x / (2 * donut_width))
    return number_donuts_x


def create_fleet(screen, donuts, width, stats):
    donut = Donut(screen)
    number_donuts_x = get_number_donuts_x(width, donut.rect.width)
    for donut_number in range(number_donuts_x):
        r = random.random()
        if r < stats.donut_level:
            create_donuts(screen, donuts, donut_number)
        else:
            pass


def update_donuts(screen, donuts, width, height, stats):
    if donuts:
        donuts.update(stats, height)
    else:
        create_fleet(screen, donuts, width, stats)
