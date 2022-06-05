import pygame.font
from dataclasses import dataclass, InitVar, field
from typing import Any


@dataclass
class Button:
    screen: Any
    message: str
    position: Any = field(default_factory=tuple)
    width: int = 200
    height: int = 50
    button_color: tuple = (0, 255, 0)
    text_color: tuple = (255, 255, 255)
    pygame.font.init()
    font: Any = pygame.font.SysFont(None, 48)
    rect: Any = pygame.Rect(0, 0, width, height)
    #rect.center = position

    def __post_init__(self):
        self.rect.center = self.position
        self.msg_image = self.font.render(self.message, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
