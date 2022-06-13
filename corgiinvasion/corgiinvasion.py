import pygame
from pygame.sprite import Group
from gamefunctions import check_event, update_screen
from corgi import Corgi, corgi_hit
from crab import update_crabs
from donuts import update_donuts
from gamestats import GameStats, Scoreboard, check_high_score, check_level_up
from button import Button


def check_collisions(stats, corgi, donuts, bullets, crabs, sb):
    """Respond to all collisions."""
    # Remove any bullets and Crab that have collided.
    pygame.sprite.groupcollide(bullets, crabs, True, True)
    # Remove any donuts that have collided with Corgi.
    eat = pygame.sprite.spritecollide(corgi, donuts, True)
    if eat:
        # Increase score.
        stats.score += 1
        sb.prep_score()
    check_high_score(stats, sb)
    # Remove any donuts that have collided with Crab.
    pygame.sprite.groupcollide(crabs, donuts, False, True)
    # Respond to Corgi being hit by Crab.
    for crab in crabs:
        if pygame.sprite.collide_mask(corgi, crab):
            corgi_hit(stats, corgi, donuts, bullets, crabs, sb)


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_width(), screen.get_height()
    pygame.display.set_caption("Corgi Invasion")
    # Set the background color.
    bg_color = (230, 230, 230)
    exit_button = Button(screen, "Exit", (screen.get_rect().centerx, screen.get_rect().centery + 50))
    play_button = Button(screen, "Play", (screen.get_rect().centerx, screen.get_rect().centery))
    level_up_button = Button(screen, "Level Up!", screen.get_rect().center)
    # Make a Corgi, Crab, a group of bullets, and a group of donuts.
    corgi = Corgi(screen)
    crabs = Group()
    bullets = Group()
    donuts = Group()
    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(corgi)
    sb = Scoreboard(screen, stats, bg_color)
    # Start the main loop for the game.
    while True:
        # Check a keyboard and mouse input.
        check_event(screen, corgi, bullets, stats, play_button, exit_button, donuts, crabs, sb)
        # Update Corgi's, his Bullet's, Crab's and Donut's moves.
        if stats.game_active:
            corgi.update()
            bullets.update(width, height)
            # Update Corgi's points and hits.
            check_collisions(stats, corgi, donuts, bullets, crabs, sb)
            update_crabs(crabs, screen, stats)
            update_donuts(screen, donuts, width, height, stats)
            check_level_up(stats, donuts, bullets, sb)
        update_screen(bg_color, screen, corgi, bullets, donuts, crabs, play_button,  exit_button, stats, sb,
                      level_up_button)


run_game()
