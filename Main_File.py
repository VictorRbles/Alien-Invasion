import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

from button import Button
from scoreboard import Scoreboard
from sound import SoundEffects

fullscreen = False

class AlienInvasion:
    # Overall class to manage game assets and behavior

    def __init__(self):
        # Initialize the game and create game resources
            
            pygame.init()
            self.settings = Settings()

            # Tell pygame to determine the size of the screen and set the screen 
            # width and height based on the players screen size
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.real_screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
                        
            pygame.display.set_caption("Luna's Alien Invasion AKA LUNA INVASION")
    
            # Create an instance to store game statistics
            self.stats = GameStats(self)
    
            # Set the background color - colors are RGB colors: amix of red, green,
            # and blue. Each color range is 0 to 255
            self.bg_color = (200, 230, 230)
    
            self.ship = Ship(self)
            self.bullets = pygame.sprite.Group()

            # Add in the aliens
            self.aliens = pygame.sprite.Group()
            self._create_fleet()

            self.play_button = Button(self.settings, self.real_screen, "Play")
            self.sb = Scoreboard(self.settings, self.real_screen, self.stats)
            pygame.mixer.init()
            self.sounds = SoundEffects()
            self.sounds.play_music_clip()


    def run_game(self):
        # Start the main loop for the game
    
        while True:
            # Call a method to check to see if any of keyboard events have occured
            self._check_events()
            # Check to see if the game is still active (more ships left)
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        global fullscreen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    # Update settings
                    self.settings.screen_width = event.w
                    self.settings.screen_height = event.h
                    self.settings.monitor_size = [event.w, event.h]
                    # Scale ship and aliens based on new window size
                    ship_width = float((event.w/pygame.display.Info().current_w) * self.ship.width)
                    ship_height = float((event.h/pygame.display.Info().current_h) * self.ship.height)
                    self.ship.scale_image(ship_width, ship_height)
                    for alien in self.aliens:
                        alien_width = float((event.w/pygame.display.Info().current_w) * alien.width)
                        alien_height = float((event.h/pygame.display.Info().current_h) * alien.height)
                        alien.scale_image(alien_width, alien_height)
                    # Update ship's screen rect and re-center at the bottom
                    self.ship.update_screen_rect(self.screen)
                    self.ship.center_ship()
                    # Update bullet size
                    self.settings.bullet_width =  float((event.w/pygame.display.Info().current_w) * self.settings.bullet_width)
                    self.settings.bullet_height = float((event.h/pygame.display.Info().current_h) * self.settings.bullet_height)
                    # Scale alien speed (example: 0.002 * width, adjust as needed)
                    self.settings.alien_speed = float((event.w/pygame.display.Info().current_w) * self.settings.alien_speed)
                    # Recreate alien fleet for new screen size
                    self.aliens.empty()
                    self._create_fleet()
            elif event.type == pygame.FULLSCREEN:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.FULLSCREEN)
                # Update settings
                self.settings.screen_width = event.w
                self.settings.screen_height = event.h
                self.settings.monitor_size = [event.w, event.h]
                # Scale ship and aliens based on new window size
                ship_width = int(event.w * 0.08)
                ship_height = int(event.h * 0.08)
                self.ship.scale_image(ship_width, ship_height)
                for alien in self.aliens:
                    alien_width = float((event.w/pygame.display.Info().current_w) * alien.width)
                    alien_height = float((event.h/pygame.display.Info().current_h) * alien.height)
                    alien.scale_image(alien_width, alien_height)
                # Update ship's screen rect and re-center at the bottom
                self.ship.update_screen_rect(self.screen)
                self.ship.center_ship()
                # Update bullet size
                self.settings.bullet_width =  float((event.w/pygame.display.Info().current_w) * self.settings.bullet_width)
                self.settings.bullet_height = float((event.h/pygame.display.Info().current_h) * self.settings.bullet_height)
                # Scale alien speed (example: 0.002 * width, adjust as needed)
                self.settings.alien_speed = float((event.w/pygame.display.Info().current_w) * self.settings.alien_speed)
                # Recreate alien fleet for new screen size
                self.aliens.empty()
                self._create_fleet()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        self.screen = pygame.display.set_mode(self.settings.monitor_size, pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        # Is the key the right arrow or is it the left arrow?
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        # Did the player hit the Q key to quit the game?
        elif event.key == pygame.K_q:
            sys.exit()
        # Did the player hit the space bar to shoot a bullet?
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        # Did the player stop holding down the arrow keys?
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # Create a new bullet and add it to the bullets group
        # Limited the number of bullets a player can have at a time by adding a
        # constant to the settings file
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sounds.play_laser_clip()

    def _update_bullets(self):
        # Update positions of the bullets and get rid of old bullets.
        self.bullets.update()
        
        # Get rid of bullets that have disappeared off the screen because they are
        # still there in the game and take up memory and execution time
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        # Respond to bullet-alien collisions
        # Check for any bullets that have hit aliens. If so, get rid of the 
        # bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            # Update score for each alien hit
            for aliens in collisions.values():
                self.stats.score += 10 * len(aliens)
                self.sounds.play_explosion_clip()
            self.sb.prep_score()
            self._check_high_score()
            self.sb.prep_high_score()
        # Check to see if the aliens group is empty and if so, create a new
        # fleet.
        if not self.aliens:
            # Destroy any existing bullets and create a new fleet
            self.bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()
            self.stats.level += 1
            self.sb.prep_level()
    
    def _update_aliens(self):
        # Update the positions of all aliens in the fleet
        # Check to see if the fleet is at an edge then update the positions of all
        # the aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("SHIP IT, LUNA!!!")
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

# Add a method to create a fleet of aliens
    def _create_fleet(self):
        """ Create a fleet of aliens """
        # Make a single alien.
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        # Determine how much space you have on the screen for aliens
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row
        aliens = Alien(self)
        # Scale the alien to match the current window size
        #alien_width = int(self.settings.screen_width * 0.08)
        #alien_height = int(self.settings.screen_height * 0.08)
        #aliens.scale_image(alien_width, alien_height)
        alien_width, alien_height = aliens.rect.size
        aliens.x = alien_width + 2 * alien_width * alien_number
        aliens.rect.x = aliens.x
        aliens.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(aliens)
    
    def _check_fleet_edges(self):
        # Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _ship_hit(self):
        # Respond to the ship being hit by an alien

        if self.stats.ships_left > 0:
            # Decrement the number of ships left
            self.stats.ships_left -= 1

            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause for half a second
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.settings.initialize_dynamic_settings() # resets speed if game over.

    def _check_aliens_bottom(self):
        # Check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # Reset the game statistics.
            self.settings.initialize_dynamic_settings() # Resets speeds
            self.stats.reset_stats()
            self.stats.game_active = True

            # Reset the scoreboard images.
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Empty the list of aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
        
    def _check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()

quit()
