import pygame
from pygame.sprite import Group
from gamefunctions import check_event, update_screen
from corgi import Corgi, corgi_hit
from crab import update_crabs
from donuts import update_donuts
from gamestats import GameStats, Scoreboard, check_high_score, check_level_up
from button import Button

lalalalalala
def check_collisions(stats, corgi, donuts, bullets, crabs, sb):
    pygame.sprite.groupcollide(bullets, crabs, True, True)
    eat = pygame.sprite.spritecollide(corgi, donuts, True)
    if eat:
        stats.score += 1
        sb.prep_score()
    check_high_score(stats, sb)
    pygame.sprite.groupcollide(crabs, donuts, False, True)
    for crab in crabs:
        if pygame.sprite.collide_mask(corgi, crab):
            corgi_hit(stats, corgi, donuts, bullets, crabs, sb)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_width(), screen.get_height()
    pygame.display.set_caption("Corgi Invasion")
    bg_color = (230, 230, 230)
    exit_button = Button(screen, "Exit", (screen.get_rect().centerx, screen.get_rect().centery + 50))
    play_button = Button(screen, "Play", (screen.get_rect().centerx, screen.get_rect().centery))
    level_up_button = Button(screen, "Level Up!", screen.get_rect().center)
    corgi = Corgi(screen)
    stats = GameStats(corgi)
    sb = Scoreboard(screen, stats, bg_color)
    crabs = Group()
    bullets = Group()
    donuts = Group()
    while True:
        check_event(screen, corgi, bullets, stats, play_button, exit_button, donuts, crabs, sb)
        if stats.game_active:
            corgi.update()
            bullets.update(width, height)
            check_collisions(stats, corgi, donuts, bullets, crabs, sb)
            update_crabs(crabs, screen, stats)
            update_donuts(screen, donuts, width, height, stats)
            check_level_up(stats, donuts, bullets, sb)
        update_screen(bg_color, screen, corgi, bullets, donuts, crabs, play_button,  exit_button, stats, sb,
                      level_up_button)


run_game()
