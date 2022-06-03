import pygame.font
from pygame.sprite import Group
from heart import Hearts


class GameStats:
    def __init__(self, corgi):
        self.reset_stats(corgi)
        self.high_score = 0
        self.read_high_score()
        self.game_active = False

    def reset_stats(self, corgi):
        self.corgi_left = corgi.hit_limit
        self.score = 0
        self.score_previous = 0
        self.level = 1
        self.level_up = False
        self.donut_level = 1.0
        self.donut_speed_level = 0.0
        self.crab_level = 0

    def read_high_score(self):
        try:
            with open('score.txt', 'r') as file:
                n = int(file.readline())
                if type(n) == int:
                    self.high_score = n
        except OSError:
            print("Could not open/read high score file")

    def write_high_score(self):
        with open('score.txt', 'w') as file:
            file.write(str(self.high_score))


class Scoreboard:
    def __init__(self, screen, stats, bg_color):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.bg_color = bg_color
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_hearts()

    def prep_score(self):
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render("Score " + score_str, True, self.text_color, self.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = self.stats.high_score
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("High score " + high_score_str, True, self.text_color, self.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_image = self.font.render("Level " + str(self.stats.level), True, self.text_color, self.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_hearts(self):
        self.hearts = Group()
        for heart_number in range(self.stats.corgi_left):
            heart = Hearts(self.screen)
            heart.rect.x = 10 + heart_number * heart.rect.width
            heart.rect.y = 10
            self.hearts.add(heart)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.hearts.draw(self.screen)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        stats.write_high_score()
        sb.prep_high_score()


def check_level_up(stats, donuts, bullets, sb):
    if stats.score == 5 * stats.level + stats.score_previous:
        stats.level_up = True
        level_change(stats, donuts, bullets, sb)


MAX_DONUT_ROW_RANDOM = 0.2
MAX_DONUT_SPEED = 2.1

def level_change(stats, donuts, bullets, sb):
    stats.level += 1
    stats.score_previous = stats.score
    sb.prep_level()
    donuts.empty()
    bullets.empty()
    if stats.donut_level > MAX_DONUT_ROW_RANDOM:
        stats.donut_level -= 0.1
    if stats.donut_speed_level < MAX_DONUT_SPEED:
        stats.donut_speed_level += 0.1
    stats.crab_level += 2
