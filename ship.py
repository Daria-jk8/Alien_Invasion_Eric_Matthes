import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
   # A ship class to store all the details related to the ship

    def __init__(self, ai_game):
      #  Initialize the ship and set its starting position
      super().__init__()

      self.settings = ai_game.settings 

      self.screen = ai_game.screen
      self.screen_rect = ai_game.screen.get_rect()
       
      # Load the ship image and get its rect. 
      self.image = pygame.image.load('images/ship.bmp')
      self.rect = self.image.get_rect()
      self.width = self.image.get_width()
      # Start each ship from the mid bottom screen 
      self.rect.midbottom = self.screen_rect.midbottom
      
      # preserving the real coordinates of the center of the ship
      self.x = float(self.rect.x)
      self.y = float(self.rect.y) # only this

      # Movement Flags
      self.moving_right = False
      self.moving_left = False 

    def update(self):
      if self.moving_right and self.rect.right < self.screen_rect.right:
        self.x += self.settings.ship_speed
      # the ship was moved to the right |§§§| --> 
      if self.moving_left and self.rect.left > 0:
        self.x -= self.settings.ship_speed
      # the ship was moved to the left |§§§| <--
      self.rect.x = self.x
      
    def blitme(self):
      # Drew the ship at its current location
      self.screen.blit(self.image, self.rect) 

    def center_ship(self):
      self.rect.midbottom = self.screen_rect.midbottom
      self.x = float(self.rect.x)    