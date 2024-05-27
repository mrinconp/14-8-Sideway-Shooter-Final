import pygame
from pygame.sprite import Sprite

class Soldier(Sprite):
    """A class for Soldiers"""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.raw = pygame.image.load('resources/soldier.bmp')
        self.image = pygame.transform.scale_by(self.raw, 0.11)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move soldier depending on direction"""
        self.y += (self.settings.soldier_speed * self.settings.army_direction)
        self.rect.y = self.y

    def check_edges(self):
        """True if a soldier reaches screen edges"""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True