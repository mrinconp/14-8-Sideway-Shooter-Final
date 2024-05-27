class Settings():
    """Set game settings"""
    
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 650
        self.bg_color = (230,230,230)

        self.max_lives = 3

        self.bullet_width = 5
        self.bullet_height = 5
        self.bullet_color = (60,60,60)
        self.bullets_max = 3

        self.army_move_speed = 50 #x_speed
        
        self.dif_rate = 1.2

        self.score_scale = 1.5

        self.reset_settings()

    def reset_settings(self):
        self.bullet_speed = 1.0
        self.shooter_speed = 0.7
        self.soldier_speed = 0.4 #y_speed
        self.soldier_points = 50

        self.army_direction = 1 #Direccion(1 down, -1 up)

    def speedup(self):
        """Increase game speed and score scale"""
        self.shooter_speed *= self.dif_rate
        self.bullet_speed *= self.dif_rate
        self.soldier_speed *= self.dif_rate

        self.soldier_points = int(self.soldier_points * self.score_scale)