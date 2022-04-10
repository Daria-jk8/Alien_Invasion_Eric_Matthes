import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # Initialise the alien and set its starting point
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # --> download pictures of aliens and assign an attribute 'rect'
        self.image = pygame.image.load("images/p_alien.png")
        self.rect = self.image.get_rect()

        # --> each new alien appears in the upper left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
     
        # --> maintaining the exact horizontal position of the alien
        self.x = float(self.rect.x) 
    
    def check_edges(self):
        # Return True if the alien is at the edge of the screen
        screen_rect = self.screen.get_rect()
        if (self.rect.right >= screen_rect.right) or (self.rect.left <= 0):
            return True 

    def update(self):
        # Move the alien
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
            
        