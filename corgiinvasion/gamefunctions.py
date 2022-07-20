import sys
import pygame
from time import sleep
from corgi import bullets_create, start_screen

MAX_BULLETS_AMOUNT = 7


def check_keydown_events(screen, event, corgi, bullets, stats, donuts, crabs, sb):
    """Respond to keypresses."""
    if event.key in {pygame.K_d, pygame.K_RIGHT}:
        corgi.moving_right = True
    elif event.key in {pygame.K_a, pygame.K_LEFT}:
        corgi.moving_left = True
    elif event.key in {pygame.K_w, pygame.K_UP}:
        corgi.moving_up = True
    elif event.key in {pygame.K_s, pygame.K_DOWN}:
        corgi.moving_back = True
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_RETURN and not stats.game_active:
        start_game(stats, donuts, bullets, crabs, corgi, sb)
    elif event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS_AMOUNT:
        bullets_create(screen, corgi, bullets)


def check_keyup_events(event, corgi):
    """Respond to key releases."""
    if event.key in {pygame.K_d, pygame.K_RIGHT}:
        corgi.moving_right = False
    elif event.key in {pygame.K_a, pygame.K_LEFT}:
        corgi.moving_left = False
    elif event.key in {pygame.K_w, pygame.K_UP}:
        corgi.moving_up = False
    elif event.key in {pygame.K_s, pygame.K_DOWN}:
        corgi.moving_back = False


def check_event(screen, corgi, bullets, stats, play_button, exit_button, donuts, crabs, sb):
    """ Check a keyboard and mouse input. """
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            check_keydown_events(screen, event, corgi, bullets, stats, donuts, crabs, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, corgi)
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not stats.game_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if play_button.rect.collidepoint(mouse_x, mouse_y):
                start_game(stats, donuts, bullets, crabs, corgi, sb)
            if exit_button.rect.collidepoint(mouse_x, mouse_y):
                sys.exit()


def score_to_screen(sb):
    """Reset Corgi's Score,Level, High Score and Hearts"""
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_hearts()


def start_game(stats, donuts, bullets, crabs, corgi, sb):
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)
    # Reset the game statistics.
    stats.reset_stats(corgi)
    stats.game_active = True
    # Reset the scoreboard images.
    score_to_screen(sb)
    # Reset the screen.
    start_screen(donuts, bullets, crabs, corgi)


def update_screen(bg_color, screen, corgi, bullets, donuts, crabs, play_button, exit_button, stats, sb,
                  level_up_button):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(bg_color)
    # Redraw all bullets, behind Corgi, donuts and Crab.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    corgi.blitme()
    donuts.draw(screen)
    crabs.draw(screen)
    # Draw the score information.
    sb.show_score()
    # Draw Play and Exit Buttons at the start of game or for the restart.
    if not stats.game_active:
        play_button.draw_button()
        exit_button.draw_button()
    # Draw Level Up Button and freeze the screen for 2 seconds, when Corgi levels up.
    if stats.level_up:
        level_up_button.draw_button()
    # Make the most recently drawn screen visible.
    pygame.display.flip()
    if stats.level_up:
        sleep(2.0)
    stats.level_up = False
