import pygame

class Ship(pygame.sprite.Sprite):
    """ A class to manage the ship """
    
    def __init__(self, ai_game_or_settings, screen=None):
        """ Initialize the ship and set its staring position """

        super().__init__()
        
        if screen is None:
            # Called with ai_game
            ai_game = ai_game_or_settings
            self.screen = ai_game.screen
            self.settings = ai_game.settings
        else:
            # Called with settings and screen (for scoreboard)
            self.settings = ai_game_or_settings
            self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Load the ship image and gets its rectangle
        self.original_image = pygame.image.load('images/ship.bmp')
        self.width = self.original_image.get_width()      # Width in pixels
        self.height = self.original_image.get_height()    # Height in pixels
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom of the center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship's position based on the movement flags. """
        # Update the ship's x value, not the rect. Make sure the ship will remain
        # in the field of view of the screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update the rect object from self x
        self.rect.x = self.x

    def blitme(self):
        """ Draw the ship at its current location """
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        # Center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def scale_image(self, width, height):
        self.image = pygame.transform.scale(self.original_image, (float(width), int(height)))
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update_screen_rect(self, new_screen):
        self.screen = new_screen
        self.screen_rect = new_screen.get_rect()