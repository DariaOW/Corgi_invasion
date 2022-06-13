import pygame.font
from pygame.sprite import Group
from heart import Hearts


class GameStats:
    """Track statistics for Corgi Invasion."""
    def __init__(self, corgi):
        """Initialize statistics."""
        self.reset_stats(corgi)
        # High score should never be reset.
        self.high_score = 0
        self.read_high_score()
        # Start game in an inactive state.
        self.game_active = False

    def reset_stats(self, corgi):
        """Initialize statistics and stats that can change during the game."""
        self.corgi_left = corgi.hit_limit
        self.score = 0
        self.score_previous = 0
        self.level = 1
        self.level_up = False
        # initialize how in/decrease the speed and number of donuts and crabs.
        self.donut_level = 1.0
        self.donut_speed_level = 0.0
        self.crab_level = 0

    def read_high_score(self):
        """Read the previously high score if possible"""
        try:
            with open('score.txt', 'r') as file:
                n = int(file.readline())
                if type(n) == int:
                    self.high_score = n
        except OSError:
            print("Could not open/read high score file")

    def write_high_score(self):
        """ Store the new high score"""
        with open('score.txt', 'w') as file:
            file.write(str(self.high_score))


class Scoreboard:
    """A class to report scoring information."""
    def __init__(self, screen, stats, bg_color):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.bg_color = bg_color
        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_hearts()

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render("Score " + score_str, True, self.text_color, self.bg_color)
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = self.stats.high_score
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("High score " + high_score_str, True, self.text_color, self.bg_color)
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render("Level " + str(self.stats.level), True, self.text_color, self.bg_color)
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_hearts(self):
        """Show how many lives of Corgi are left."""
        self.hearts = Group()
        for heart_number in range(self.stats.corgi_left):
            heart = Hearts(self.screen)
            heart.rect.x = 10 + heart_number * heart.rect.width
            heart.rect.y = 10
            self.hearts.add(heart)

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw hearts.
        self.hearts.draw(self.screen)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        stats.write_high_score()
        sb.prep_high_score()


def check_level_up(stats, donuts, bullets, sb):
    """Check to see if there's a new level."""
    if stats.score == 5 * stats.level + stats.score_previous:
        stats.level_up = True
        level_change(stats, donuts, bullets, sb)


MAX_DONUT_ROW_RANDOM = 0.2
MAX_DONUT_SPEED = 2.1


def level_change(stats, donuts, bullets, sb):
    """ Update parameters for new level"""
    stats.level += 1
    stats.score_previous = stats.score
    sb.prep_level()
    # Empty donuts and bullets.
    donuts.empty()
    bullets.empty()
    # Check the limits for speed and number of donuts.
    if stats.donut_level > MAX_DONUT_ROW_RANDOM:
        stats.donut_level -= 0.1
    if stats.donut_speed_level < MAX_DONUT_SPEED:
        stats.donut_speed_level += 0.1
    stats.crab_level += 2
