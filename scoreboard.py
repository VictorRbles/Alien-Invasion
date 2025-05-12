import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_high_score()
        self.prep_level()
        self.prep_score()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.ai_settings.bg_color
        )

        # Place the score halfway between high score (center) and level (right)
        self.score_rect = self.score_image.get_rect()
        left = self.high_score_rect.right
        right = self.level_rect.left
        self.score_rect.centerx = (left + right) // 2
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.ai_settings.bg_color
        )

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.ai_settings.bg_color
        )

        # Position at the top right.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = 20

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        # Use the height of the score text for the ship icon size
        ship_height = self.score_rect.height
        # Maintain the ship image's aspect ratio
        ship_aspect = Ship(self.ai_settings, self.screen).original_image.get_width() / Ship(self.ai_settings, self.screen).original_image.get_height()
        ship_width = int(ship_height * ship_aspect)

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            #scale the ship image
            ship.image = pygame.transform.scale(ship.original_image, (ship_width, ship_height))
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
            ship.rect.y = 15
            self.ships.add(ship)

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw ships.
        self.ships.draw(self.screen)