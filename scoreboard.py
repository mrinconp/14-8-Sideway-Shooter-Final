import pygame.font
from pygame.sprite import Group

from shooter import Shooter

class Scoreboard():
    """A class to record scores"""
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None, 48)
        
        self.prep_images()
        
    def prep_images(self):
        """Render text to image and add hearts"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        """Render score to image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_scoreboard(self):
        """Show scores and draw lives left"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect) 
        self.screen.blit(self.level_image, self.level_rect)
        self.lives.draw(self.screen)

    def prep_high_score(self):
        """Render high score to image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                            self.text_color, self.settings.bg_color)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check if there's a new high score"""
        if self.stats.score >= self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Render level to image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):
        """Show lives left"""
        self.lives = Group()
        for lives in range(self.stats.lives_left):
            heart = Shooter(self.game, "heart", scale=0.035)
            heart.rect.x = 15 + lives* heart.rect.width
            heart.rect.y = 10
            self.lives.add(heart)