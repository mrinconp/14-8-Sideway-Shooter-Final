import pygame
import sys
from time import sleep

from settings import Settings
from shooter import Shooter
from bullet import Bullet
from soldier import Soldier
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class SidewayShooter:
    def __init__(self):
        """Initialize the game and create resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Sideway Shooter")

        self.stats = GameStats(self)
        self.shooter = Shooter(self, scale=0.15)
        self.bullets = pygame.sprite.Group()
        self.soldiers = pygame.sprite.Group()
        self.button_play = Button(self, "Play")
        self.sb = Scoreboard(self)

        self._create_army()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.shooter.update()
                self._update_bullets()
                self._update_soldiers()
            self._update_screen()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.shooter.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.sb.show_scoreboard()
        self.soldiers.draw(self.screen)

        if not self.stats.game_active:
            self.button_play.draw_button()

        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.button_play.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.reset_settings()
            self._start_game()
            self.sb.prep_images()

    def _start_game(self):
        """Reset game settings and start a new game."""
        self.stats.reset_stats()
        self.stats.game_active = True

        self.soldiers.empty()
        self.bullets.empty()

        self._create_army()
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.shooter.moving_down = True
        elif event.key == pygame.K_DOWN:
            self.shooter.moving_up = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._shoot_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.shooter.moving_down = False
        elif event.key == pygame.K_DOWN:
            self.shooter.moving_up = False

    def _shoot_bullet(self):
        """Fire a new bullet if the limit is not reached yet."""
        if len(self.bullets) < self.settings.bullets_max:
            nueva_bullet = Bullet(self)
            self.bullets.add(nueva_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old ones."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_soldier_collisions()

    def _check_bullet_soldier_collisions(self):
        """Respond to bullet-soldier collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.soldiers, True, True)
        if collisions:
            for soldiers in collisions.values():
                self.stats.score += self.settings.soldier_points * len(soldiers)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.soldiers:
            self.bullets.empty()
            self._create_army()
            self.settings.speedup()

            self.stats.level += 1
            self.sb.prep_level()

    def _update_soldiers(self):
        """Check if the army is at an edge, then update the positions of all soldiers in the army."""
        self._check_army_edges()
        self.soldiers.update()

        if pygame.sprite.spritecollideany(self.shooter, self.soldiers):
            self._soldier_reached()

        self._check_soldiers_margin()

    def _create_army(self):
        """Create an army of soldiers."""
        soldier = Soldier(self)
        soldier_width, soldier_height = soldier.rect.size
        available_space_y = self.settings.screen_height - soldier_height
        soldiers_number_y = available_space_y // (2 * soldier_height)

        shooter_width = self.shooter.rect.width
        available_space_x = self.settings.screen_width - 2 * shooter_width
        amount_columns = available_space_x // (2 * soldier_width)

        for col_number in range(amount_columns):
            for soldier_number in range(soldiers_number_y):
                self._create_soldier(soldier_number, col_number)

    def _create_soldier(self, soldier_number, col_number):
        """Create a soldier and place it in the row."""
        soldier = Soldier(self)
        soldier_width, soldier_height = soldier.rect.size
        soldier.x = self.settings.screen_width - 2 * soldier_width - soldier_width * col_number
        soldier.rect.x = soldier.x
        soldier.y = soldier_height + soldier_height * soldier_number
        soldier.rect.y = soldier.y

        self.soldiers.add(soldier)

    def _check_army_edges(self):
        """Respond if any soldiers have reached an edge."""
        for soldier in self.soldiers.sprites():
            if soldier.check_edges():
                self._change_direction()
                break

    def _change_direction(self):
        """Drop the entire army and change the army's direction."""
        for soldier in self.soldiers.sprites():
            soldier.rect.x -= self.settings.army_move_speed
        self.settings.army_direction *= -1

    def _soldier_reached(self):
        """Respond to the shooter being hit by a soldier."""
        if self.stats.lives_left > 0:
            self.stats.lives_left -= 1
            self.sb.prep_lives()

            self.soldiers.empty()
            self.bullets.empty()

            self._create_army()
            self.shooter.center_shooter()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_soldiers_margin(self):
        """Check if any soldiers have reached the left side of the screen."""
        for soldier in self.soldiers.sprites():
            if soldier.rect.left <= 0:
                self._soldier_reached()
                break

if __name__ == '__main__':
    ss = SidewayShooter()
    ss.run_game()
