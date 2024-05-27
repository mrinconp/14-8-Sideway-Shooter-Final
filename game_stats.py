class GameStats():
    def __init__(self, game):
        self.settings  = game.settings
        self.game_active = False
        self.high_score = 0

        self.reset_stats()

    def reset_stats(self):
        self.lives_left = self.settings.max_lives
        self.score = 0
        self.level = 1