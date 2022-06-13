import pygame
from pygame.sprite import Sprite
from time import sleep


class Corgi(Sprite):
    def __init__(self, screen):
        super(Corgi, self).__init__()
        self.screen = screen
        # Load the Corgi image, and get its rect.
        self.image = pygame.transform.scale(pygame.image.load('images/corgi.bmp'), (100, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Movement flags.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_back = False
        # Limits for movements and hits.
        self.hit_limit = 3       # number of Corgis lives.
        self.speed_factor = 1    # number of movements per one keyboards input.

    def blitme(self):
        """Draw the Corgi at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the Corgi's position, based on movement flags."""
        if self.moving_right:
            self.rect.centerx += self.speed_factor
        if self.moving_left:
            self.rect.centerx -= self.speed_factor
        if self.moving_up:
            self.rect.bottom -= self.speed_factor
        if self.moving_back:
            self.rect.bottom += self.speed_factor
        # Keep a Corgi within the window.
        self.rect.clamp_ip(self.screen_rect)

    def center_corgi(self):
        """Center the Corgi on the screen."""
        self.rect.centerx = self.screen_rect.centerx


def start_screen(donuts, bullets, crabs, corgi):
    # Empty the list of donuts, crabs and bullets.
    donuts.empty()
    bullets.empty()
    crabs.empty()
    # Center the Corgi.
    corgi.center_corgi()


def corgi_hit(stats, corgi, donuts, bullets, crabs, sb):
    """Respond to Corgi being hit by Crab."""
    if stats.corgi_left > 0:
        # Decrement Corgi's lives.
        stats.corgi_left -= 1
        # Update scoreboard.
        sb.prep_hearts()
        # Reset the screen.
        start_screen(donuts, bullets,crabs, corgi)
        # Freeze the screen for 2 seconds.
        sleep(2.0)
    else:
        # End the Game and reset to start screen.
        stats.game_active = False
        pygame.mouse.set_visible(True)


class Bullet(Sprite):
    """A class to manage bullets fired from the Corgi."""
    def __init__(self, screen, bullet_width, bullet_height, rect_center, direction_up, direction_right):
        """Create a bullet object, at the Corgi's current position."""
        Sprite.__init__(self)
        self.screen = screen
        self.speed_factor = 1
        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        # Create bullet rect at (0, 0), then set correct position.
        self.rect = pygame.Rect(0, 0, self.bullet_width, self.bullet_height)
        self.rect.center = rect_center
        # Store a decimal value for the bullet's position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.color = (0, 255, 0)
        self.direction_up = direction_up
        self.direction_right = direction_right

    def update(self, width, height):
        """Move the bullet up the screen."""
        if self.direction_up and not self.direction_right:
            # Update the decimal position of the bullet.
            self.y -= self.speed_factor
            # Update the rect position.
            self.rect.y = self.y
        elif not self.direction_up and not self.direction_right:
            self.y += self.speed_factor
            self.rect.y = self.y
        elif self.direction_right and not self.direction_up:
            self.x += self.speed_factor
            self.rect.x = self.x
        elif self.direction_right and self.direction_up:
            self.x -= self.speed_factor
            self.rect.x = self.x
        # Delete bullets outside the screen.
        if self.rect.y < 0 or self.rect.y > height or self.rect.x > width or self.rect.x < 0:
            self.kill()

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)


def bullets_create(screen, corgi, bullets):
    """Create bullets for four directions and add to bullets group."""
    new_bullet_up = Bullet(screen, 3, 15, corgi.rect.center, True, False)
    new_bottom_bullet = Bullet(screen, 3, 15, corgi.rect.center, False, False)
    new_right_bullet = Bullet(screen, 15, 3, corgi.rect.center, False, True)
    new_left_bullet = Bullet(screen, 15, 3, corgi.rect.center, True, True)
    bullets.add(new_bullet_up)
    bullets.add(new_bottom_bullet)
    bullets.add(new_right_bullet)
    bullets.add(new_left_bullet)
