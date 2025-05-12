import pygame

class Settings:
    """ A class to store all settings for Alien Invasion """

    def __init__(self):
        """ Initialize the game's settings """
        # Screen settings
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.bg_color = (255, 255, 255)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings - dark grey bullets that are 3 pixels wide and 15
        # pixelds high. Bullets travel slower than the ship.
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        
        self.speedup_scale = 1.1  # How quickly the game speeds up

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1.0
        self.fleet_direction = 1  # 1 means right, -1 means left

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale