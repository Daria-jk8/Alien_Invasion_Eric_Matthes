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

class AlienInvasion:

    def __init__(self):
        # Initialise the game and create game resources"
        pygame.init()
        self.settings = Settings() 

        self.screen = pygame.display.set_mode((1200, 800)) # pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, 'PLAY')

        pygame.display.set_caption("Alien Invasion") 
        
        # Create an instance to store the game stats
        # and create a scoreboard (sb)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

    def _update_bullets(self):
        # Update the positions of bullets and delete old bullets 
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
           # print(len(self.bullets))         
        self._check_bullet_allien_collosions()   
    
    def _check_bullet_allien_collosions(self):    
        # Check for any bullets that have hit an alien   
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy the existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase the level
            self.stats.level += 1
            self.sb.prep_level()

        if collisions:
          for aliens in collisions.values():  
              self.stats.score += self.settings.alien_points * len(aliens)
          self.sb.prep_score()
          self.sb.check_high_score() 

    def _fire_bullet(self):
        # Create a new bullet instance and add it to the group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
 
    def _create_fleet(self):
        # Create a new fleet of aliens
        # --> creating an alien and counting the number of aliens in a row
        # --> the interval between the aliens is equal to the width of the alien
        alien = Alien(self)
        alien_widht, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_widht)
        number_aliens_x = available_space_x // (2 * alien_widht)

        # --> determine the number of lines that are placed on the screen
        ship_height = self.ship.rect.height
        availavle_space_y = (self.settings.screen_height - (3 * ship_height) - ship_height)
        number_rows = availavle_space_y // (2 * alien_height)

        # --> creation the fleet
        for row_number in range(number_rows):
            # --> creation of the first row of aliens
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
          
    def _create_alien(self, alien_number, row_number):      
           # --> creating an alien and placing it in a row
           alien = Alien(self)
           alien_widht, alien.height = alien.rect.size
           alien.x = alien_widht + 2 * alien_widht * alien_number
           alien.rect.x = alien.x
           alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
           self.aliens.add(alien)

    def _update_aliens(self):
        # --> update all alien positions
        self._check_fleet_edges()
        self.aliens.update()       
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
          # print(" Ship hit !!!")
          self._ship_hit()
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()  
        
    def _check_aliens_bottom(self):
        # Check if alien has reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
        
    def _check_fleet_edges(self):
        # Respond appropriately if an alien has reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
               self._change_fleet_direction()
               break

    def _change_fleet_direction(self):    
        # Drop Entire fleet and change the fleet direction
        for alien in self.aliens.sprites():
          alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1  

    def _ship_hit(self):
        # Respond to ship being hit by an alien
        if self.stats.ships_left > 0: 
           self.stats.ships_left -= 1
           self.sb.prep_ships()

           self.aliens.empty()
           self.bullets.empty()

           self._create_fleet()
           self.ship.center_ship()
           # Pause
           sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_play_button(self, mouse_pos):
        # --> Start a new game when the player clicks 'PLAY'
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Initialize dynamic settings
            self.settings.initialize_dynamic_settings() # --> reset game settings
            # Hide the mouse cursor
            pygame.mouse.set_visible(False)
            # Reset the game stats and activate the game 
            self.stats.resert_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Get rid of any remaining alien or bullets
            self.aliens.empty()
            self.bullets.empty()

           # self._create_fleet()
           # self.ship.center_ship()
    
    def _update_screen(self):
        # Redraw the screen during each pass through the loop
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
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _check_events(self):
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
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False 

    def _check_keydown_events(self, event):
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_LEFT: 
                self.ship.moving_left = True 
            elif event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_SPACE:  
                self._fire_bullet()            
    
    def run_game(self):
        while True:               # --> main Cycle
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets() 
                self._update_aliens()

            self._update_screen()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()            
