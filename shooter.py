import pygame
from pygame.sprite import Sprite

class Shooter(Sprite):
    """A class for Shooter and its lives"""
    def __init__(self, game, object = "shooter", scale = 1):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        image_paths = {"shooter": 'resources/shooter.bmp',
                        "heart": 'resources/heart.bmp'}

        self.raw = pygame.image.load(image_paths[object])        
        self.scale = scale
        self.image = pygame.transform.scale_by(self.raw, self.scale) #Escala
        self.rect = self.image.get_rect()

        self.rect.midleft = self.screen_rect.midleft
        self.y = self.rect.y

        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update position based on moving flags"""
        if self.moving_up and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.shooter_speed

        if self.moving_down and self.rect.top > 0:
            self.y -= self.settings.shooter_speed

        self.rect.y = self.y

    def blitme(self):
        """Draw object in position"""
        self.screen.blit(self.image, self.rect)

    def center_shooter(self):
        self.rect.midleft = self.screen_rect.midleft
        self.y = self.rect.y