import pygame


class Settings:
    def __init__(self):
        # --> Initialize the game's static settings

        # --> Display/Screen 
        self.screen_width =  1200
        self.screen_height =  800 
        self.bg_color = (230, 230, 230) # -->light gray color
        # --> ship 
        self.ship_limit = 3
        # --> bullet 
        self.bullet_weight = 7 # --> very powerful bullet 30 or 300 or 3000
        self.bullet_height = 17
        self.bullet_color = (28, 129, 55)
        self.bullets_allowed = 10
        # --> alien 
        self.fleet_drop_speed = 10
        # --> the pace of acceleration of the game
        # --> How quickly the alien point value increases
        self.speedup_scale = 1.5
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # --> variable settings
        self.ship_speed = 5 / self.speedup_scale
        self.bullet_speed = 5 / self.speedup_scale
        self.alien_speed = 1.0 / self.speedup_scale
        # fleet_direction = 1 moved to right; and -1 - left
        self.fleet_direction = 1
        self.alien_points = 50 // self.score_scale

    def increase_speed(self):
        self.ship_speed *=  self.speedup_scale
        self.bullet_speed *=  self.speedup_scale
        self.alien_speed *=  self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
   